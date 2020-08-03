import random

import pygame

import config
from DisplayEngine import GUIDisplayEngine
from agent import AStarAgent
from qLearning import *
from util import manhattanDistance


class Game:
    def __init__(self, board_size, obstacle_chance, board_file=None, agent=None):
        self.board = Board(board_size, obstacle_chance, board_file)
        # self.agent = AStarAgent(lambda x: manhattanDistance(x.snake[0], x.fruit_location))
        self.agent = agent
        self.state = None
        pass

    def run(self):

        # self.state = config.GameState.PAUSED
        self.state = config.GameState.RUNNING
        self.board.spawn_snake(2, 2, 1)
        self.board.spawn_fruit()
        display = GUIDisplayEngine(self.board.move)
        while self.state != config.GameState.GAME_OVER:
            pygame.display.update()
            display.render(self)
            if self.state == config.GameState.PAUSED:
                continue

            ## q learning shit
            current_state = self.agent.get_current_state(self.board)
            fruit_x = self.board.fruit_location[0]
            fruit_y = self.board.fruit_location[1]

            snake_x_before = self.board.snake[0][0]
            snake_y_before = self.board.snake[0][1]
            board_size = self.board.board_size

            fruit_relative_x_before = cyclic(fruit_x - snake_x_before, board_size)
            fruit_relative_y_before = cyclic(fruit_y - snake_y_before, board_size)

            move = self.agent.next_move(self.board)
            if move:
                self.board.next_move = move
            self.board.step()
            # time.sleep(0.1)
            pygame.display.update()

            new_state = self.agent.get_current_state(self.board)

            if self.board.snake[0] in self.board.obstacles or self.board.snake[0] in self.board.snake[1:]:
                self.state = config.GameState.GAME_OVER
                self.agent.update(current_state, self.agent.find_action(move), new_state, -100)
            # self.agent.update_values(current_state, new_state, -1, self.agent.find_action(move))

            elif self.board.snake[0] == self.board.fruit_location:
                if len(self.board.snake) > pow(self.board.board_size, 2) - 1:
                    self.state = config.GameState.GAME_OVER
                    self.agent.update(current_state, self.agent.find_action(move), new_state, 50)
                else:
                    self.board.eat_fruit()
                    self.agent.update(current_state, self.agent.find_action(move), new_state, 30)
            # self.agent.update_values(current_state, new_state, 1, self.agent.find_action(move))

            elif len(self.board.snake) >= pow(self.board.board_size, 2) - 1:
                self.state = config.GameState.GAME_OVER
                self.agent.update(current_state, self.agent.find_action(move), new_state, 50)

            else:
                snake_x_after = self.board.snake[0][0]
                snake_y_after = self.board.snake[0][1]

                fruit_relative_x_after = cyclic(fruit_x - snake_x_after, board_size)
                fruit_relative_y_after = cyclic(fruit_y - snake_y_after, board_size)

                if fruit_relative_x_after <= fruit_relative_x_before and fruit_relative_y_after <= fruit_relative_y_before:
                    self.agent.update(current_state, self.agent.find_action(move), new_state, 1)
                else:
                    self.agent.update(current_state, self.agent.find_action(move), new_state, -1)
            # self.agent.update_values(current_state, new_state, -0.1, self.agent.find_action(move))

            # else:
            # 	self.agent.update_values(current_state, new_state, -0.1, self.agent.find_action(move))

            display.render(self)
            display.clock.tick(config.FRAME_RATE)
        self.board.end_game()
    # self.agent.print_table()


class Board:
    def __init__(self, board_size, obstacle_chance, board_file=None):
        self.board_size = board_size
        self.next_move = config.Direction.LEFT
        self.snake = []
        self.obstacles = set()
        self.fruit_location = ()
        if board_file:
            self.load_from_file(board_file)
        else:
            # generate a new board
            self.generate_obstacles(board_size, obstacle_chance, self.load_obstacles('ob.txt'))

    def move(self, direction):
        self.next_move = direction

    @staticmethod
    def load_obstacles(filename):
        """
        Loads and returns obstacles from file
        file format:
            * Each line represents one obstacle
            * x and y are separated by "," and segments are separated  by "_"
        """
        with open(f'data/obstacles/{filename}') as file:
            return [[[int(c) for c in b.split(',')] for b in a.split('_')] for a in file.readlines()]

    def load_from_file(self, file_name):
        with open(f'data/boards/{file_name}') as file:
            _board = [line.split(',') for line in file.readlines()]
            if not _board:
                return
            for i in range(len(_board)):
                for j in range(len(_board[0])):
                    if _board[i][j] == 'x':
                        self.obstacles.add((i, j))

    def save_to_file(self, file_name):
        with open(f'data/boards/{file_name}', 'w') as file:
            _board = [['_'] * self.board_size for _ in range(self.board_size)]
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if (i, j) in self.obstacles:
                        _board[i][j] = 'x'
            file.write('\n'.join([','.join(line) for line in _board]))

    def generate_obstacles(self, board_size, obstacle_chance, obstacles):
        """
        Generate obstacle from list of obstacles randomly placed throughout the board
        :param board_size:
        :param obstacle_chance: number of tiles count as obstacle
        :param obstacles: list of obstacles
        :return: board with randomly generated obstacles
        """
        all_obstacles = []
        for i in range(int(board_size / 4) + 1):
            for j in range(int(board_size / 4) + 1):
                if random.random() > obstacle_chance:
                    continue
                cell_i = 4 * i
                cell_j = 4 * j
                curr_i = random.randint(1, 2)
                curr_j = random.randint(1, 2)
                ob = random.choice(obstacles)
                ob = [(row + curr_j + cell_j, col + curr_i + cell_i) for row, col in ob]
                ob = [(row, col) for row, col in ob if row < board_size and col < board_size]
                all_obstacles += ob
        self.obstacles = all_obstacles[:]

    def spawn_snake(self, row, col, length):
        """
        Spawns a snake where the head's coordinates are (row, col) and with body length of `length` (including the head)
        """
        head = (row, col)
        self.snake = [head]
        if head in self.obstacles:
            self.obstacles.remove(head)
        for i in range(1, length):
            part = (row, col + i)
            if part in self.obstacles:
                self.obstacles.remove(part)
            self.snake.append(part)

    def step(self):
        head_i, head_j = self.snake[0]
        direction = self.next_move
        if direction == config.Direction.LEFT:
            head_j -= 1
        elif direction == config.Direction.RIGHT:
            head_j += 1
        elif direction == config.Direction.UP:
            head_i -= 1
        elif direction == config.Direction.DOWN:
            head_i += 1

        head_i = (head_i + self.board_size) % self.board_size
        head_j = (head_j + self.board_size) % self.board_size

        if (head_i, head_j) != self.fruit_location:
            self.snake.pop()

        self.snake.insert(0, (head_i, head_j))

    def spawn_fruit(self):
        """
        add fruit to random location on the board
        """
        i = random.randint(0, config.BOARD_SIZE - 1)
        j = random.randint(0, config.BOARD_SIZE - 1)

        while (i, j) in self.obstacles or (i, j) in self.snake:
            i = random.randint(0, config.BOARD_SIZE - 1)
            j = random.randint(0, config.BOARD_SIZE - 1)
        self.fruit_location = (i, j)

    def eat_fruit(self):
        self.spawn_fruit()

    def end_game(self):
        # board.save_to_file('b.txt')
        print(f'Game Ended, Score: {len(self.snake)}')

    def __repr__(self):
        s = ''
        for i in range(self.board_size):
            for j in range(self.board_size):
                if (i, j) in self.obstacles:
                    s += 'x '
                elif self.snake and (i, j) == self.snake[0]:
                    s += '@ '
                elif self.snake and (i, j) in self.snake:
                    s += 'O '
                elif self.fruit_location == (i, j):
                    s += '$ '
                else:
                    s += '_ '
            s += '\n'
        return s

    def __eq__(self, other):
        return isinstance(other, Board) and other.snake[0] == self.snake[0]


def score_helper(scores, num):
    scores_sum = sum(scores)
    counter = 0
    for i in scores:
        if i >= num:
            counter += 1

    return (counter/scores_sum) * 100



if __name__ == '__main__':
    pygame.init()
    agent = QLearningAgent(0.9, 0.85, 0.05)
    scores = []
    top_score = 0
    agent.read_qtable()


    for i in range(6000):

        game = Game(config.BOARD_SIZE, 0, agent=agent)

        game.run()
        score = len(game.board.snake)
        if score > top_score:
            top_score = score
        scores.append(score)
        print(str(i) + ' top score: ' + str(top_score) + ' half board: ' + str(score_helper(scores, 18)) + '%')
        agent.write_qtable()
    game.agent.print_table()
    print(scores)

    config.FRAME_RATE = 10

    game = Game(config.BOARD_SIZE, 0, agent=agent)

    game.run()
    game.run()
    game.run()
