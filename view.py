"""
Handle drawing stuff to the screen
"""
#Import modules
import pygame
from pygame.locals import *
# import pylab
# import numpy
#Import our own other files 
from curve import *
from Model import *
from Control import *


pygame.font.init()
fontsmall = pygame.font.SysFont('UbuntuMono',20)
fontlarge = pygame.font.SysFont('UbuntuMono',100)
fontmedium = pygame.font.SysFont('UbuntuMono',40)
fonttiny = pygame.font.SysFont('UbuntuMono', 15)


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

		# Display some text
		font = pygame.font.Font(None, 18)
		self.line_text = font.render("Input Line", 1, (0, 0, 255))
		self.derivative_text = font.render("Derivative", 1, (160, 32, 240))
		self.integral_text = font.render("Integral", 1, (0 ,120, 0))

		# Blit everything to the screen
		self.screen.blit(self.line_text, (self.screen_size[0]-60, 10))
		self.screen.blit(self.derivative_text, (self.screen_size[0]-60, 30))
		self.screen.blit(self.integral_text, (self.screen_size[0]-60, 50))


	def display_text(self, msg, font, color, x, y):
		"""Writes text on screen"""
		text = font.render(msg, True, color)
		self.screen.blit(text, [x, y])
	        
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
				pygame.draw.lines(self.screen, (0, 0, 255), False, self.controller.running_points, 2)
			except ValueError: #If there are not enough points in lines (in the beginning of drawing)
				pass

		#Draw the curves
		if self.controller.curve:
			pygame.draw.lines(self.screen, (0, 0, 255), False, self.controller.curve.line.points, 3)
			pygame.draw.lines(self.screen, (160, 32, 240), False, self.controller.curve.derivative.points, 3)
			pygame.draw.lines(self.screen, (0 ,120, 0), False, self.controller.curve.integral.points, 3)

			# Displaying the pull points:
			if self.controller.pull_mode == "Handle":
				for pt in self.controller.curve.line.pull_points:
					pt_int = (int(pt[0]), int(pt[1]))
					pygame.draw.circle(self.screen, (0,0,0), pt_int, 3)

		#Draw the tangent lines
		if self.controller.mode == 'Show tangent':
			try:
				pygame.draw.lines(self.screen, (0, 200, 255), False, self.controller.curve.line.tangent, 3)
			except TypeError:
				print type(self.controller.curve.line.tangent)

		if self.controller.mode == 'Show area':
			pygame.draw.polygon(self.screen,(0, 200, 255),self.controller.curve.line.area,0)

		#Display the open cv image on screen
		if self.controller.mode == 'Open CV drawing':
			if self.controller.image != None:
				image=pygame.surfarray.make_surface(self.controller.image)
				image.set_alpha(150) #255 is fully opaque, 0 is fully transparent
				self.screen.blit(image,(0, 0))

		#display the current mode 
		self.display_text('Current mode: {}'.format(self.controller.mode),fontsmall, (186,85,211), 0,0) #purple color
		#display the instructions for the mode underneath the mode name
		instructions = self.get_instructions_for_mode(self.controller.mode)
		self.display_text(instructions,fontsmall,(186,85,211), 0, 30)

		pygame.display.update()

	def get_instructions_for_mode(self, mode):
		if mode == 'Show tangent':
			return 'click on a point to show tangent.'
		if mode == 'Open CV drawing':
			return 'Open CV drawing color: {}'.format(color)


		


