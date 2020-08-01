import random

import pygame

import config
from DisplayEngine import GUIDisplayEngine
from agent import AStarAgent

from util import manhattanDistance


class Game:
	def __init__(self, board_size, obstacle_chance, board_file=None):
		self.board = Board(board_size, obstacle_chance, board_file)
		self.agent = AStarAgent(self.board, lambda x: manhattanDistance(self.board.snake[0], self.board.fruit_location))
		self.state = None
		pass

	def run(self):

		self.state = config.GameState.PAUSED
		self.board.spawn_snake(2, 2, 3)
		self.board.spawn_fruit()
		display = GUIDisplayEngine(self.board.move)
		while self.state != config.GameState.GAME_OVER:
			pygame.display.update()
			display.render(self)
			if self.state == config.GameState.PAUSED:
				continue
			move = self.agent.next_move()
			if move:
				self.board.next_move = move
			self.board.step()
			# time.sleep(0.1)
			pygame.display.update()

			if self.board.snake[0] in self.board.obstacles or self.board.snake[0] in self.board.snake[1:]:
				self.state = config.GameState.GAME_OVER
			display.clock.tick(1)
		self.board.end_game()


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
		else:
			print(('WRTHbfjk.dbvujl0asb.kasvbndli'))

		head_i = (head_i + self.board_size) % self.board_size
		head_j = (head_j + self.board_size) % self.board_size

		if (head_i, head_j) != self.fruit_location:
			self.snake.pop()
		else:
			self.eat_fruit()

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
					s += '$'
				else:
					s += '_ '
			s += '\n'
		return s

	def __eq__(self, other):
		return isinstance(other, Board) and other.snake == self.snake


if __name__ == '__main__':
	pygame.init()
	game = Game(config.BOARD_SIZE, 0)
	game.run()
	pass
