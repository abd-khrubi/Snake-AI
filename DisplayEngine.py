import config
import pygame


class DisplayEngine:
	def render(self, board):
		raise Exception('Unimplemented')


class CliDisplayEngine(DisplayEngine):

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


class GUIDisplayEngine(DisplayEngine):
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((config.GUI_HEIGHT, config.GUI_WIDTH))
		self.clock = pygame.time.Clock()

		self.screen.fill((0, 0, 0))

	def render(self, board):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		self.screen.fill((0, 0, 0))
		block_size = config.BLOCK_SIZE
		for row in range(config.GUI_HEIGHT):
			for col in range(config.GUI_WIDTH):
				rect = pygame.Rect(
					row * block_size, col * block_size, block_size,
					block_size
				)
				pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
		for row in range(config.BOARD_SIZE):
			for col in range(config.BOARD_SIZE):
				i = row * block_size
				j = col * block_size
				rect = pygame.Rect(j, i, block_size, block_size)
				if (row, col) == board.snake[0]:
					# draw head
					pygame.draw.rect(self.screen, (0, 0, 225), rect)
					pass
				elif (row, col) in board.snake:
					pygame.draw.rect(self.screen, (255, 0, 255), rect)
					# draw body part
					pass
				elif (row, col) in board.obstacles:
					pygame.draw.rect(self.screen, (255, 0, 0), rect)
					# draw obstacle
					pass

		pygame.display.update()


if __name__ == '__main__':
	disp = GUIDisplayEngine()
	disp.screen.fill((0, 0, 0))
	while 1:
		disp.render(None)
# pygame.display.update()
