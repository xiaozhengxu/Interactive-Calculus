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
	Class for displaying curves.
	"""

	def __init__(self, curve=None):
		pygame.init()
		self.screen_size = (1000, 1000)
		self.screen = pygame.display.set_mode(self.screen_size)
		self.controller = Controller()

		

	def draw_grid(self):
		"""
		Method to draw grid if user wants
		"""
		
		
		for i in range(0, self.screen_size[0], 20):
			pygame.draw.line(self.screen, (128,128,128), (i, 0), (i, self.screen_size[1]), 1)
		for j in range(0, self.screen_size[1], 20):
			pygame.draw.line(self.screen, (128,128,128), (0, j), (self.screen_size[0], j), 1)

	

	def draw_graph(self):
		"""
		Draws the axes 
		"""
		
		#draw the x and y axes
		pygame.draw.line(self.screen, (0, 0, 0), (self.screen_size[0]/2, 0), (self.screen_size[0]/2, self.screen_size[1]), 3)
		pygame.draw.line(self.screen, (0, 0, 0), (0, self.screen_size[1]/2), (self.screen_size[0], self.screen_size[1]/2), 3)

	def draw_legend(self):
		"""
		Draws the legend
		"""
# Fill background
		# background = pygame.Surface((100, 100))
		# background = background.convert()
		# background.fill((250, 250, 250))

		# Display some text
		font = pygame.font.Font(None, 18)
		self.line_text = font.render("Input Line", 1, (0, 0, 255))
		self.derivative_text = font.render("Derivative", 1, (160, 32, 240))
		self.integral_text = font.render("Integral", 1, (0 ,120, 0))
		# textpos = text.get_rect()
		# textpos.centerx = background.get_rect().centerx
		# background.blit(text, textpos)

		# # # Blit everything to the screen
		self.screen.blit(self.line_text, (self.screen_size[0]-60, 10))
		self.screen.blit(self.derivative_text, (self.screen_size[0]-60, 30))
		self.screen.blit(self.integral_text, (self.screen_size[0]-60, 50))
		#pygame.display.flip()
		#self.controller.model.legend_redraw = False

		
		# freetype = pygame.font.SysFont("serif", 14)
  #       self.line_legend = freetype.render("Line", True, (0, 0, 255))
  #       self.derivative_legend = freetype.render("Derivative", True, (160, 32, 240))
  #       self.integral_legend = freetype.render("Integral", True, (0, 255, 0))
  #       self.screen.blit(self.line_legend, (0, 20)) 
  #       self.screen.blit(self.derivative_legend, (0, 40)) 
  #       self.screen.blit(self.integral_legend, (0, 60)) 		self.screen.blit(text, (0, 40))
  		#self.screen.blit(text, (self.screen_size[0], 40))


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



		if self.controller.curve:
			pygame.draw.lines(self.screen, (0, 0, 255), False, self.controller.curve.line.points, 3)
			pygame.draw.lines(self.screen, (160, 32, 240), False, self.controller.curve.derivative.points, 3)
			pygame.draw.lines(self.screen, (0 ,120, 0), False, self.controller.curve.integral.points, 3)

			if self.controller.pull_mode == "Handle":
				for pt in self.controller.curve.line.pull_points:
					pt_int = (int(pt[0]), int(pt[1]))
					pygame.draw.circle(self.screen, (0,0,0), pt_int, 3)
		pygame.display.update()



		


