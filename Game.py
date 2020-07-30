import random
class Game:
	def __init__(self):
		self.board = []
		pass

	def clone(self):
		pass


class Board:
	def __init__(self, board_size, obstacle_chance, board_file=None):
		self.board = [['_'] * board_size for _ in range(board_size)]
		if board_file:
			self.load_from_file(board_file)
		else:
			# generate a new board
			self.generate_obstacles(board_size, obstacle_chance, self.load_obstacles('ob.txt'))

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

	def generate_obstacles(self, board_size, obstacle_chance, obstacles):
		"""
		Generate obstacle from list of obstacles randomly placed throughout the board
		:param board_size:
		:param obstacle_chance: number of tiles count as obstacle
		:param obstacles: list of obstacles
		:return: board with randomly generated obstacles
		"""
		all_obstacles = []
		for i in range(int(board_size / 4)):
			for j in range(int(board_size / 4)):
				if random.random() > obstacle_chance:
					continue
				cell_i = 4 * i
				cell_j = 4 * j
				curr_i = random.randint(1, 2)
				curr_j = random.randint(1, 2)
				ob = random.choice(obstacles)
				ob = [(col + curr_i + cell_i, row + curr_j + cell_j) for row, col in ob]
				all_obstacles += ob
		for x, y in all_obstacles:
			self.board[y][x] = 'x'

	def __repr__(self):
		return '\n'.join([' '.join(a) for a in self.board])


if __name__ == '__main__':
	board = Board(24, 1)
	print(board)
	pass
