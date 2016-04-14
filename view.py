"""
Handle drawing stuff to the screen
"""
#Import modules
import pygame
from pygame.locals import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
import numpy
import time
#Import our own other files 
from curve import *
from Control import *
class View(object):
	"""

	"""

	def __init__(self, curve=None):
		pygame.init()
		self.screen = pygame.display.set_mode((1000, 1000))
		#screen = pygame.display.get_surface()
		# self.curve = curve
		self.controller=Controller()
	   # self.grid_mode = grid

	def draw_grid(self):
		for i in range(0, 1000, 20):
			pygame.draw.line(self.screen, (128,128,128), (i, 0), (i, 1000), 1)
			pygame.draw.line(self.screen, (128,128,128), (0, i), (1000, i), 1)

	def draw_line(self):
		pass

	def draw_graph(self, grid):

		self.screen.fill(pygame.Color('white'))

		if grid == True: #and self.grid_status == False:
			self.draw_grid()   

		pygame.draw.line(self.screen, (0, 0, 0), (500, 0), (500, 1000), 3)
		pygame.draw.line(self.screen, (0, 0, 0), (0, 500), (1000, 500), 3)

	def draw_input(self):
		'''Displays the user's drawing input on the screen'''
		
		self.controller.handle_events()
		# print self.controller.curve

		if self.controller.curve:# len(self.controller.running_points)>1:
			pygame.draw.lines(self.screen, (255, 0, 0), False, self.controller.curve.line.points, 2)
			pygame.draw.lines(self.screen, (0, 255, 0), False, self.controller.curve.derivative.points, 2)
			pygame.draw.lines(self.screen, (0 ,0 ,255), False, self.controller.curve.integral.points, 2)

		else: 
			self.screen.fill(pygame.Color('white'))
			self.draw_graph(grid=True)

		pygame.display.update()

	def draw(self, grid):
		if 'graph_drawn' not in globals():
			self.draw_graph(self, grid)
			graph_drawn == True

		if graph_drawn == False:
			self.draw_graph(self, grid)
			graph_drawn == True

		draw_input()


		


