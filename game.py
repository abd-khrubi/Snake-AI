import enum
import random
import time

from DisplayEngine import DisplayEngine, CliDisplayEngine
from agent import Agent


class Direction(enum.Enum):
	LEFT = 1
	RIGHT = 2
	UP = 3
	DOWN = 4


class GameState:
	RUNNING = 1
	PAUSED = 2
	ENDED = 3


class Game:
	def __init__(self, board_size, obstacle_chance, board_file=None):
		self.board = Board(board_size, obstacle_chance, board_file)
		self.agent = Agent(self.board)
		self.state = None
		pass

	def run(self):
		self.state = GameState.RUNNING
		while self.state != GameState.ENDED:
			if self.state == GameState.PAUSED:
				continue
			next_dir = self.agent.next_move()
			self.board.step(next_dir)

		print(f'Game Ended, Score: {len(self.board.snake)}')


class Board:
	def __init__(self, board_size, obstacle_chance, board_file=None):
		self.board_size = board_size
		self.snake = []
		self.obstacles = set()
		if board_file:
			self.load_from_file(board_file)
		else:
			# generate a new board
			self.generate_obstacles(board_size, obstacle_chance, self.load_obstacles('ob.txt'))

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

	def step(self, direction):
		head_i, head_j = self.snake[0]

		if direction == Direction.LEFT:
			head_j -= 1
		elif direction == Direction.RIGHT:
			head_j += 1
		elif direction == Direction.UP:
			head_i -= 1
		elif direction == Direction.DOWN:
			head_i += 1

		head_i = (head_i + self.board_size) % self.board_size
		head_j = (head_j + self.board_size) % self.board_size
		if (head_i, head_j) in self.obstacles or (head_i, head_j) in self.snake:
			self.end_game()
		self.snake.insert(0, (head_i, head_j))
		self.snake.pop()

	def end_game(self):
		print("Lost!!!!!")

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
				else:
					s += '_ '
			s += '\n'
		return s


if __name__ == '__main__':
	board = Board(8, 1)
	display: DisplayEngine = CliDisplayEngine()
	# print(board)
	board.spawn_snake(2, 2, 3)
	# print(board)
	while True:
		board.step(Direction.LEFT)
		# print(board)
		display.render(board)
		time.sleep(1)
		pass
	# board.save_to_file('b.txt')
	pass
