from game import Board


class Graph:
	def __init__(self, board):
		self.board = board
		self.size = board.board_size * board.board_size
		self.graph = [[0 for _ in range(self.size)] for _ in range(self.size)]
		self.V = self.size
		# self.graph = dict()
		# self.generate_graph()

		# self.path = self.hamiltonian_cycle(0, [])
	def is_safe(self, v, pos, path):
		if self.graph[path[pos - 1]][v] == 0:
			return False
		for vertex in path:
			if vertex == v:
				return False
		return True

	def ham_util(self, path, pos):
		if pos == self.V:
			if self.graph[path[pos - 1]][path[0]] == 1:
				return True
			else:
				return False
		for v in range(1, self.V):
			if self.is_safe(v, pos, path):
				path[pos] = v
			if self.ham_util(path, pos + 1):
				return True
		return False

	def ham(self):
		path = [-1] * self.V
		path[0] = 0
		if not self.ham_util(path, 1):
			return False
		print(path)
		return True
	# def generate_graph(self):
	# 	for row in range(self.board.board_size):
	# 		for col in range(self.board.board_size):
	# 			if not self.check_legal(row, col):
	# 				continue
	# 			v = col + row * self.board.board_size
	# 			e = set()
	# 			if self.check_legal(row - 1, col):  # up
	# 				e.add(self.get_pos(row - 1, col))
	# 			if self.check_legal(row + 1, col):  # down
	# 				e.add(self.get_pos(row + 1, col))
	# 			if self.check_legal(row, col - 1):  # left
	# 				e.add(self.get_pos(row, col - 1))
	# 			if self.check_legal(row, col + 1):  # right
	# 				e.add(self.get_pos(row, col + 1))
	# 			self.graph[v] = e
	#
	# def hamiltonian_cycle1(self, pt, path: list):
	# 	if pt not in set(path):
	# 		path = path + [pt]
	# 		if len(path) == self.size:
	# 			return path
	# 		for pt_next in self.graph.get(pt, []):
	# 			res_path = path[:]
	# 			candidates = self.hamiltonian_cycle(pt_next, res_path)
	# 			if candidates is not None:
	# 				return candidates

	def check_legal(self, row, col):
		# row = (row + self.board.board_size) % self.board.board_size
		# col = (col + self.board.board_size) % self.board.board_size
		if row < 0 or row >= self.board.board_size or col < 0 or col >= self.board.board_size:
			return False
		return (row, col) not in self.board.obstacles

	def get_pos(self, row, col):
		row = (row + self.board.board_size) % self.board.board_size
		col = (col + self.board.board_size) % self.board.board_size
		return col + row * self.board.board_size


if __name__ == '__main__':
	board: Board = Board(3, 0)
	# board.obstacles = [(0, 1), (1, 1)]
	graph = Graph(board)
	print(graph.size)
	graph.ham()
	# print(graph.path)
