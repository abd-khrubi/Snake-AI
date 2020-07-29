from copy import deepcopy
import random


class Game:
	def __init__(self):
		self.board = []
		pass

	def clone(self):
		pass


class Board:
	def __init__(self, board_size, board_file=None):
		self.board = [['_'] * board_size for _ in range(board_size)]
		if board_file:
			self.load_from_file(board_file)
		else:
			# generate a new board
			obstacles = self.generate_obstacles(board_size, 3, self.load_obstacles('ob.txt'))
			for x, y in obstacles:
				self.board[y][x] = 'x'

	def load_obstacles(self, filename):
		"""
		Loads and returns obstacles from file
		file format:
			* Each line represents one obstacle
			* x and y are separated by "," and segments are separated  by "_"
		"""
		with open(f'data/obstacles/{filename}') as file:
			return [[[int(c) for c in b.split(',')] for b in a.split('_')] for a in file.readlines()]

	def load_from_file(self, file_name):
		with open(file_name) as file:
			self.board = [line.split(',') for line in file.readlines()]

	def save_to_file(self, file_name):
		with open(file_name, 'w') as file:
			file.write('\n'.join([','.join(line) for line in self.board]))

	def generate_obstacles(self, board_size, obstacle_count, obstacles):
		"""
		Generate obstacle from list of obstacles randomly placed throughout the board
		:param board_size:
		:param obstacle_count: number of tiles count as obstacle
		:param obstacles: list of obstacles
		:return: board with randomly generated obstacles
		"""
		all_obstacles = []
		count = 0
		while count < obstacle_count:
			obstacle = random.choice(obstacles)
			i = random.randint(1, board_size - max(obstacle, key=lambda ob: ob[0])[0])
			j = random.randint(1, board_size - max(obstacle, key=lambda ob: ob[1])[1])

			my_obstacle = [(x + i, y + j) for x, y in obstacle]
			if not self.is_legal_obstacle(my_obstacle, all_obstacles):
				continue
			# all_obstacles.append(my_obstacle)
			all_obstacles += my_obstacle
			count += 1
		return all_obstacles

	def is_legal_obstacle(self, obstacle, my_obstacles):
		"""

		:param obstacle: an array of the obstacle's coordinates
		:param my_obstacles: an array of all the placed obstacles' coordinates
		:return:
		"""
		for x, y in obstacle:
			for ob_x, ob_y in my_obstacles:
				if x - 1 <= ob_x <= x + 1:
					return False
				if y - 1 <= ob_y <= y + 1:
					return False
		return True

	def __repr__(self):
		return '\n'.join([' '.join(a) for a in self.board])


if __name__ == '__main__':
	board = Board(15)
	print(board)
	pass
