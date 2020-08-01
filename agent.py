from copy import deepcopy

from config import Direction
from util import PriorityQueueWithFunction, cyclic, manhattanDistance


class State:
	def __init__(self, board, g, heu_function, path):
		self.board = board
		self.h = heu_function(board)
		self.g = g
		self.f = self.h + self.g
		self.path = path

	def is_goal(self):
		return self.board.snake[0] == self.board.fruit_location

	def get_legal_action(self):
		board_size = self.board.board_size
		legal_actions = {Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN}
		i, j = self.board.snake[0]
		if (cyclic(i - 1, board_size), j) in self.board.obstacles or (cyclic(i - 1, board_size), j) in self.board.snake:
			legal_actions.remove(Direction.DOWN)
		if (cyclic(i + 1, board_size), j) in self.board.obstacles or (cyclic(i + 1, board_size), j) in self.board.snake:
			legal_actions.remove(Direction.UP)
		if (i, cyclic(j - 1, board_size)) in self.board.obstacles or (i, cyclic(j - 1, board_size)) in self.board.snake:
			legal_actions.remove(Direction.LEFT)
		if (i, cyclic(j + 1, board_size)) in self.board.obstacles or (i, cyclic(j + 1, board_size)) in self.board.snake:
			legal_actions.remove(Direction.RIGHT)

		return list(legal_actions)

	def __eq__(self, other):
		return other.board == self.board

	def __hash__(self) -> int:
		return hash(self.board)


class Agent:
	def __init__(self, board):
		self.board = board

	def next_move(self):
		raise Exception('Method not implemented!')


class AStarAgent(Agent):
	def __init__(self, board, heuristics):
		super().__init__(board)
		self.heuristic_function = heuristics
		self.moves = []

	def next_move(self):
		if not self.moves:
			self.moves = self.search(self.board)
			if not self.moves:
				return None
		return self.moves.pop()

	def search(self, init_board):
		fringe = PriorityQueueWithFunction(lambda state: state.f)

		init_state = State(init_board, 0, self.heuristic_function, [])
		fringe.push(init_state)

		visited = []

		while not fringe.isEmpty():
			item: State = fringe.pop()
			if item in visited:
				continue

			if item.is_goal():
				return item.path

			for move in item.get_legal_action():
				new_board = deepcopy(item.board)
				new_board.next_move = move
				new_board.step()
				new_state = State(new_board, item.g + 1, self.heuristic_function, item.path + [move])
				fringe.push(new_state)
		return []
