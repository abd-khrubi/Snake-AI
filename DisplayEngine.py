import config
import pygame

from config import Direction, GameState


# from pygame_input import Inputs, Button


class DisplayEngine:
	def __init__(self, input_cb):
		"""

		:param input_cb: takes direction
		"""
		self.input_cb = input_cb

	def render(self, game):
		raise Exception('Unimplemented')


class CliDisplayEngine(DisplayEngine):  # TODO game not board

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
			print(s)  #


class GUIDisplayEngine(DisplayEngine):
	def __init__(self, input_cb):
		super().__init__(input_cb)
		pygame.init()
		self.screen = pygame.display.set_mode((config.GUI_HEIGHT, config.GUI_WIDTH))
		self.clock = pygame.time.Clock()

		self.screen.fill((0, 0, 0))

	def render(self, game):
		board = game.board
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if game.state == GameState.PAUSED:
					game.state = GameState.RUNNING
				if event.key == pygame.K_LEFT and board.next_move != config.Direction.RIGHT:
					self.input_cb(config.Direction.LEFT)
				elif event.key == pygame.K_UP and board.next_move != config.Direction.DOWN:
					self.input_cb(config.Direction.UP)
				elif event.key == pygame.K_DOWN and board.next_move != config.Direction.UP:
					self.input_cb(config.Direction.DOWN)
				elif event.key == pygame.K_RIGHT and board.next_move != config.Direction.LEFT:
					self.input_cb(config.Direction.RIGHT)

		self.screen.fill((0, 0, 0))
		block_size = config.BLOCK_SIZE
		# for row in range(config.BOARD_SIZE):
		# 	for col in range(config.BOARD_SIZE):
		# 		rect = pygame.Rect(
		# 			row * block_size, col * block_size, block_size,
		# 			block_size
		# 		)
		# 		pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
		for row in range(config.BOARD_SIZE):
			for col in range(config.BOARD_SIZE):
				i = row * block_size
				j = col * block_size
				rect = pygame.Rect(j, i, block_size, block_size)
				if (row, col) == board.snake[0]:
					# draw head
					pygame.draw.rect(self.screen, (0, 0, 225), rect)

				elif (row, col) == board.fruit_location:
					# draw fruit
					pygame.draw.rect(self.screen, (0, 255, 0), rect)
				elif (row, col) in board.snake:
					pygame.draw.rect(self.screen, (255, 0, 255), rect)
				# draw body part

				elif (row, col) in board.obstacles:
					pygame.draw.rect(self.screen, (255, 0, 0), rect)
				# draw obstacle

	# pygame.display.update()


if __name__ == '__main__':
	disp = GUIDisplayEngine()
	disp.screen.fill((0, 0, 0))
	while 1:
		disp.render(None)
# pygame.display.update()
