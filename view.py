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
from Model import *
from Control import *

class View(object):
	"""

	"""

	def __init__(self, curve=None):
		pygame.init()
		self.screen = pygame.display.set_mode((1000, 1000))
		self.controller = Controller()

		

	def draw_grid(self):
		"""
		Method to draw grid if user wants
		"""
		
		for i in range(0, 1000, 20):
			pygame.draw.line(self.screen, (128,128,128), (i, 0), (i, 1000), 1)
			pygame.draw.line(self.screen, (128,128,128), (0, i), (1000, i), 1)


	def draw_graph(self):
		"""
		Draws the axes 
		"""
		
		#draw the x and y axes
		pygame.draw.line(self.screen, (0, 0, 0), (500, 0), (500, 1000), 3)
		pygame.draw.line(self.screen, (0, 0, 0), (0, 500), (1000, 500), 3)

	def draw_legend(self):
		pass

	def draw(self):
		"""
		Displays the user's drawing input on the screen
		"""
		
		self.controller.handle_events()

		#NOTE: Redrawn every time to handle curve movement
		self.screen.fill(pygame.Color('white'))
		if self.controller.model.grid_status:	# True, False, 
			self.draw_grid()
		if self.controller.model.legend_status:	# True, False, 
			self.draw_legend()
		self.draw_graph()

		if self.controller.mode == 'Mouse drawing':
			try:
				pygame.draw.lines(self.screen, (255, 0, 0), False, self.controller.running_points, 2)
			except ValueError:
				pass

		if self.controller.curve:
			pygame.draw.lines(self.screen, (255, 0, 0), False, self.controller.curve.line.points, 2)
			pygame.draw.lines(self.screen, (0, 255, 0), False, self.controller.curve.derivative.points, 2)
			pygame.draw.lines(self.screen, (0 ,0, 255), False, self.controller.curve.integral.points, 2)

			if self.controller.pull_mode == "Handle":
				for pt in self.controller.curve.line.pull_points:
					pt_int = (int(pt[0]), int(pt[1]))
					pygame.draw.circle(self.screen, (0,0,0), pt_int, 3)

		if self.controller.mode == 'Open CV drawing':
			if self.controller.image != None:
				image=pygame.surfarray.make_surface(self.controller.image)
				image.set_alpha(150) #255 is fully opaque, 0 is fully transparent
				self.screen.blit(image,(0, 0))

		pygame.display.update()



		


