class DisplayEngine:
	def __init__(self):
		pass

	def render(self, board):
		raise Exception('Unimplemented')


class CliDisplayEngine(DisplayEngine):
	def __init__(self):
		DisplayEngine.__init__(self)

	def render(self, board):
		s = ''
		for i in range(board.board_size):
			for j in range(board.board_size):
				if (i, j) in board.obstacles:
					s += 'x '
				elif board.snake and (i, j) == board.snake[0]:
					s += '@ '
				elif board.snake and (i, j) in board.snake:
					s += 'O '
				else:
					s += '_ '
			s += '\n'
			print(s)
