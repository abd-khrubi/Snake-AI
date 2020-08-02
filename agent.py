from copy import deepcopy

from config import Direction
from util import PriorityQueueWithFunction, cyclic


class State:
	def __init__(self, board, g, heu_function, path):
		self.board = board
		self.h = heu_function(board)
		self.g = g
		self.f = self.h + self.g
		self.path = path

	def is_goal(self):
		return self.board.snake[0] == self.board.fruit_location

	def _is_legal_move(self, i, j):
		board_size = self.board.board_size
		i = cyclic(i, board_size)
		j = cyclic(j, board_size)
		return \
			0 <= i < board_size and 0 <= j < board_size \
			and (i, j) not in self.board.obstacles and (i, j) not in self.board.snake

	def get_legal_action(self):
		legal_actions = {Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN}
		i, j = self.board.snake[0]
		if not self._is_legal_move(i - 1, j):
			legal_actions.remove(Direction.UP)
		if not self._is_legal_move(i + 1, j):
			legal_actions.remove(Direction.DOWN)
		if not self._is_legal_move(i, j - 1):
			legal_actions.remove(Direction.LEFT)
		if not self._is_legal_move(i, j + 1):
			legal_actions.remove(Direction.RIGHT)

		return list(legal_actions)

	def __eq__(self, other):
		return other.board == self.board

	def __hash__(self) -> int:
		return hash(self.board)


class Agent:

	def next_move(self, board):
		raise Exception('Method not implemented!')


class AStarAgent(Agent):
	def __init__(self, heuristics):
		self.heuristic_function = heuristics
		self.moves = []

	def next_move(self, board):
		if not self.moves:
			self.moves = self.search(board)
			if not self.moves:
				return None
		return self.moves.pop()

	def search(self, init_board):
		fringe = PriorityQueueWithFunction(lambda state: state.f)

		init_state = State(init_board, 0, self.heuristic_function, [])
		fringe.push(init_state)

		visited = []

		while not fringe.isEmpty():
			# print(f'Open: {len(fringe)}, Close: {len(visited)}')
			item: State = fringe.pop()
			if item in visited:
				continue
			visited.append(item)
			if item.is_goal():
				return item.path

			for move in item.get_legal_action():
				new_board = deepcopy(item.board)
				new_board.next_move = move
				new_board.step()
				new_state = State(new_board, item.g + 1, self.heuristic_function, [move] + item.path)
				fringe.push(new_state)
		return []
