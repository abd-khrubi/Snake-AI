import config
import pygame

from config import Direction

# from pygame_input import Inputs, Button


class DisplayEngine:
	def __init__(self, input_cb):
		"""

		:param input_cb: takes direction
		"""
		self.input_cb = input_cb

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
	def __init__(self, input_cb):
		super().__init__(input_cb)
		pygame.init()
		self.screen = pygame.display.set_mode((config.GUI_HEIGHT, config.GUI_WIDTH))
		self.clock = pygame.time.Clock()

		self.screen.fill((0, 0, 0))
		#
		# inputs = Inputs()
		# inputs['left'] = Button(pygame.K_LEFT)
		# inputs['left'].on_press(lambda x: self.input_cb(config.Direction.LEFT))
		# inputs['up'] = Button(pygame.K_UP)
		# inputs['up'].on_press(lambda x: self.input_cb(config.Direction.UP))

	def render(self, board):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.input_cb(config.Direction.LEFT)
				elif event.key == pygame.K_UP:
					self.input_cb(config.Direction.UP)
				if event.key == pygame.K_DOWN:
					self.input_cb(config.Direction.DOWN)
				elif event.key == pygame.K_RIGHT:
					self.input_cb(config.Direction.RIGHT)

		self.screen.fill((0, 0, 0))
		block_size = config.BLOCK_SIZE
		for row in range(config.BOARD_SIZE):
			for col in range(config.BOARD_SIZE):
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

		# pygame.display.update()


if __name__ == '__main__':
	disp = GUIDisplayEngine()
	disp.screen.fill((0, 0, 0))
	while 1:
		disp.render(None)
# pygame.display.update()
