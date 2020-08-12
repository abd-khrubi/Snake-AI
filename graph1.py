import numpy as np

from util import cyclic


class ConnectedComponent:
	def __init__(self, board):
		self._board = np.zeros([board.board_size, board.board_size])
		self.ccMap = np.zeros_like(self._board)
		self.total_cc = 0
		self.visited = np.zeros_like(self._board, dtype=bool)
		self.board = board
		self.board_size = board.board_size

		self.cc_data = dict()

		self.generate_board()
		self.generate_cc_map()

	def generate_board(self):
		self._board = np.zeros([self.board_size, self.board_size])
		for i, j in self.board.snake[1:] + self.board.obstacles:
			self._board[i, j] = 1

	def generate_cc_map(self):
		self.ccMap = np.zeros_like(self._board)
		self.cc_data = dict()
		self.total_cc = 0
		for i in range(self.board_size):
			for j in range(self.board_size):
				if self._board[i, j] == 1 or self.ccMap[i, j] != 0:
					continue
				self.total_cc += 1
				size = self.fill_cc(i, j, self.total_cc)
				self.cc_data[self.total_cc] = size

	def fill_cc(self, row, col, cc):
		row = cyclic(row, self.board_size)
		col = cyclic(col, self.board_size)
		if self._board[row, col] != 0 or self.ccMap[row, col] != 0:
			return 0
		self.ccMap[row, col] = cc

		return \
			1 + \
			self.fill_cc(row - 1, col, cc) + \
			self.fill_cc(row + 1, col, cc) + \
			self.fill_cc(row, col - 1, cc) + \
			self.fill_cc(row, col + 1, cc)

	def cc_size(self, row, col):
		cc = self.ccMap[row, col]
		if cc == 0:
			return -1
		return self.cc_data[cc]
		# self.visited = np.zeros_like(self._board, dtype=bool)
		# cc = self.ccMap[row, col]
		# if cc == 0:
		# 	return -1
		# return self._cc_size(row, col, cc)

	def _cc_size(self, row, col, cc):
		row = cyclic(row, self.board_size)
		col = cyclic(col, self.board_size)
		if self.visited[row, col] or self.ccMap[row, col] != cc:
			return 0
		self.visited[row, col] = True
		return \
			1 + \
			self._cc_size(row - 1, col, cc) + self._cc_size(row + 1, col, cc) + \
			self._cc_size(row, col - 1, cc) + self._cc_size(row, col + 1, cc)
