from game import Board


class Agent:
	def __init__(self, board: Board):
		self.board = board

	def next_move(self):
		raise Exception('Method not implemented!')
