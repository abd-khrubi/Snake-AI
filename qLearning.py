import random, math
from agent import Agent
from config import Direction
from qlearning_game import *
from util import cyclic, Counter
import util


class QLearningAgent(Agent):

    def __init__(self, alpha, gamma, random_rate):
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor
        self.random_rate = random_rate
        # self.actions_space = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]
        self.actions_space = [0, 1, 2, 3]
        self.q_table = dict()

        self.values = Counter()  # Q(s, a)

    def get_current_state_head(self, board):
        """
        DIDNT USE... Check the 3 blocks around the head of the snake
        :param board:
        :return:
        """
        # 3 places around head
        snake = board.snake
        snake_x = snake[0][0]
        snake_y = snake[0][1]
        fruit_position = board.fruit_location
        board_size = board.board_size
        fruit_x = cyclic(fruit_position[0], board_size)
        fruit_y = cyclic(fruit_position[1], board_size)

        direction = board.next_move

        left = right = up = 0

        state_name = ""

        if direction == Direction.LEFT:
            left = (snake_x, cyclic(snake_y + 1, board_size))
            up = (cyclic(snake_x - 1, board_size), snake_y)
            right = (snake_x, cyclic(snake_y - 1, board_size))

        elif direction == Direction.RIGHT:
            left = (snake_x, cyclic(snake_y - 1, board_size))
            up = (cyclic(snake_x + 1, board_size), snake_y)
            right = (snake_x, cyclic(snake_y + 1, board_size))

        elif direction == Direction.UP:
            left = (cyclic(snake_x - 1, board_size), snake_y)
            up = (snake_x, cyclic(snake_y - 1, board_size))
            right = (cyclic(snake_x + 1, board_size), snake_y)

        elif direction == Direction.DOWN:
            left = (cyclic(snake_x + 1, board_size), snake_y)
            up = (snake_x, cyclic(snake_y + 1, board_size))
            right = (cyclic(snake_x - 1, board_size), snake_y)

        if left == fruit_position:
            state_name = "1"
        elif left in snake:
            state_name = "2"
        else:
            state_name = "0"

        if up == fruit_position:
            state_name += ",1"
        elif up in snake:
            state_name += ",2"
        else:
            state_name += ",0"

        if right == fruit_position:
            state_name += ",1"
        elif right in snake:
            state_name += ",2"
        else:
            state_name += ",0"

        state_name += ',' + str(cyclic(snake_x - fruit_x, board_size))
        state_name += ',' + str(cyclic(snake_y - fruit_y, board_size))

        return state_name

    def get_current_state(self, board):
        """
        Check the 4 blocks around the head of the snake for obstacles
        And check where the fruit is located relative to the head of the snake (NW, N, NE, E, SE, S, SW, W)
        :param board:
        :return:
        """
        snake = board.snake
        snake_x = snake[0][0]
        snake_y = snake[0][1]
        fruit_position = board.fruit_location
        board_size = board.board_size
        # fruit_x = cyclic(fruit_position[0], board_size)
        # fruit_y = cyclic(fruit_position[1], board_size)
        fruit_x = fruit_position[0]
        fruit_y = fruit_position[1]

        up = 1 if (snake_x, cyclic(snake_y - 1, board_size)) in snake or (
        snake_x, cyclic(snake_y - 1, board_size)) in board.obstacles else 0
        down = 1 if (snake_x, cyclic(snake_y + 1, board_size)) in snake or (
        snake_x, cyclic(snake_y + 1, board_size)) in board.obstacles else 0
        left = 1 if (cyclic(snake_x - 1, board_size), snake_y) in snake or (
        cyclic(snake_x - 1, board_size), snake_y) in board.obstacles else 0
        right = 1 if (cyclic(snake_x + 1, board_size), snake_y) in snake or (
        cyclic(snake_x + 1, board_size), snake_y) in board.obstacles else 0

        state_name = str(left) + str(up) + str(right) + str(down)

        fruit_relative_x = fruit_x - snake_x
        fruit_relative_y = fruit_y - snake_y

        if fruit_relative_x < 0 and fruit_relative_y < 0:
            state_name += '10000000'

        elif fruit_relative_x == 0 and fruit_relative_y < 0:
            state_name += '01000000'

        elif fruit_relative_x > 0 and fruit_relative_y < 0:
            state_name += '00100000'

        elif fruit_relative_x > 0 and fruit_relative_y == 0:
            state_name += '00010000'

        elif fruit_relative_x > 0 and fruit_relative_y > 0:
            state_name += '00001000'

        elif fruit_relative_x == 0 and fruit_relative_y > 0:
            state_name += '00000100'

        elif fruit_relative_x < 0 and fruit_relative_y > 0:
            state_name += '00000010'

        elif fruit_relative_x < 0 and fruit_relative_y == 0:
            state_name += '00000001'

        # state_name += ',' + str(cyclic(fruit_relative_x, board_size)) + str(cyclic(fruit_relative_y, board_size))

        return state_name

    def get_current_state_ol(self, board): ##NOT USED
        game_board: Board = board  # TODO remove this line
        snake = game_board.snake
        fruit_position = game_board.fruit_location

        fruit_relative_position = [fruit_position[i] - snake[0][i] for i in range(len(fruit_position))]

        while fruit_relative_position[0] < 0:
            fruit_relative_position[0] += len(snake)

        while fruit_relative_position[0] > len(snake):
            fruit_relative_position[0] -= len(snake)

        while fruit_relative_position[1] < 0:
            fruit_relative_position[1] += len(snake)

        while fruit_relative_position[1] > len(snake):
            fruit_relative_position[1] -= len(snake)

        state_name = str(fruit_relative_position[0]) + ',' + str(fruit_relative_position[1])

        tail_relative_position = [snake[len(snake) - 1][i] - snake[0][i] for i in range(len(snake[0]))]

        while tail_relative_position[0] < 0:
            tail_relative_position[0] += len(snake)

        while tail_relative_position[0] > len(snake):
            tail_relative_position[0] -= len(snake)

        while tail_relative_position[1] < 0:
            tail_relative_position[1] += len(snake)

        while tail_relative_position[1] > len(snake):
            tail_relative_position[1] -= len(snake)

        state_name += ',' + str(tail_relative_position[0]) + ',' + str(tail_relative_position[1])

        return state_name

    def next_move(self, board):
        current_state = self.get_current_state(board)
        action = self.getAction(current_state)

        if action == 0:
            return Direction.LEFT
        elif action == 1:
            return Direction.RIGHT
        elif action == 2:
            return Direction.UP
        elif action == 3:
            return Direction.DOWN
        return action

    def find_action(self, action):
        if action == Direction.LEFT:
            return 0
        elif action == Direction.RIGHT:
            return 1
        elif action == Direction.UP:
            return 2
        else:
            return 3

    def getLegalActions(self, state):
        """
          Get the actions available for a given
          state. This is what you should use to
          obtain legal actions for a state
        """
        return self.actions_space

    def update(self, state, action, nextState, reward):
        """
            The parent class calls this to observe a
            state = action => nextState and reward transition.
            You should do your Q-Value update here

            NOTE: You should never call this function,
            it will be called on your behalf
        """
        self.values[(state, action)] += self.alpha * (
                reward + self.gamma * self.getValue(nextState) - self.values[(state, action)])

    def getQValue(self, state, action):
        """
        Returns Q(state,action)
        Should return 0.0 if we never seen
        a state or (state,action) tuple
        """
        return self.values[(state, action)]

    def getValue(self, state):
        """
            Returns max_action Q(state,action)
            where the max is over legal actions.  Note that if
            there are no legal actions, which is the case at the
            terminal state, you should return a value of 0.0.
        """
        actions = self.getLegalActions(state)
        if not actions:
            return 0
        return max([self.getQValue(state, a) for a in actions])

    def getPolicy(self, state):
        """
            Compute the best action to take in a state.  Note that if there
            are no legal actions, which is the case at the terminal state,
            you should return None.
        """
        val = self.getValue(state)
        actions = [a for a in self.getLegalActions(state) if self.getQValue(state, a) == val]
        if not actions:
            return None
        return random.choice(actions)

    def getAction(self, state):
        """
            Compute the action to take in the current state.  With
            probability self.epsilon, we should take a random action and
            take the best policy action otherwise.  Note that if there are
            no legal actions, which is the case at the terminal state, you
            should choose None as the action.

            HINT: You might want to use util.flipCoin(prob)
            HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legal_actions = self.getLegalActions(state)
        action = None
        if util.flipCoin(self.random_rate):
            if legal_actions:
                action = random.choice(legal_actions)
        else:
            action = self.getPolicy(state)
        return action

    def write_qtable(self, path='qtable.txt'):
        f = open(path, 'w')
        for k, v in self.values.items():
            f.write(str(k[0]) + ':' + str(k[1]) + ':' + str(v) + '\n')
        # f.write(str(self.values))
        f.close()

    def read_qtable(self, path='qtable.txt'):
        f = open(path, 'r')
        line = f.readline()
        while line:
            # print(line)
            line = line.strip('\n')
            line = line.split(':')
            print(line)
            self.values[(line[0], float(line[1]))] = float(line[2])
            line = f.readline()
        print(self.values)

    def print_table(self):
        print(self.values)

    def reset(self):
        pass
