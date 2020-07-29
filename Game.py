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
			pass
		pass

	def load_from_file(self, file_name):
		with open(file_name) as file:
			self.board = [line.split(',') for line in file.readlines()]

	def save_to_file(self, file_name):
		with open(file_name, 'w') as file:
			file.write('\n'.join([','.join(line) for line in self.board]))
