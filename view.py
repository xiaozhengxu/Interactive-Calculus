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
		self.line_text = font.render("Input Line", 1, (0, 153, 76))
		self.derivative_text = font.render("Derivative", 1, (0 ,0, 153))
		self.integral_text = font.render("Integral", 1, (153, 0, 0))

		# Find legend coordinates
		der_pos = (self.controller.curve.derivative.points[-1][0] + 5, self.controller.curve.derivative.points[-1][1])
		line_pos = (self.controller.curve.line.points[-1][0] + 5, self.controller.curve.line.points[-1][1])
		int_pos = (self.controller.curve.integral.points[-1][0] + 5, self.controller.curve.integral.points[-1][1])


		# Blit everything to the screen
		self.screen.blit(self.line_text, line_pos)
		self.screen.blit(self.derivative_text, der_pos)
		self.screen.blit(self.integral_text, int_pos)


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
			if self.controller.curve:	
				self.draw_legend()
			
		self.draw_graph()

		if self.controller.mode['Mouse drawing']:
			try:
				pygame.draw.lines(self.screen, (0 , 153, 76), False, self.controller.running_points, 2)
			except ValueError: #If there are not enough points in lines (in the beginning of drawing)
				pass

		#Draw the curves
		if self.controller.curve:
			pygame.draw.lines(self.screen, (0, 153, 76), False, self.controller.curve.line.points, 3)
			pygame.draw.lines(self.screen, (0, 0, 153), False, self.controller.curve.derivative.points, 3)
			pygame.draw.lines(self.screen, (153, 0, 0), False, self.controller.curve.integral.points, 3)

			# Displaying the pull points:
			if self.controller.pull_mode == "Handle":
				for pt in self.controller.curve.line.pull_points:
					pt_int = (int(pt[0]), int(pt[1]))
					pygame.draw.circle(self.screen, (0,0,0), pt_int, 3)

		#Draw the tangent lines
		if self.controller.mode['Show tangent']:
			try:
				pygame.draw.lines(self.screen, (0, 200, 255), False, self.controller.curve.line.tangent, 3)
			except TypeError: #if a tangent is not created, don't draw.
				# print type(self.controller.curve.line.tangent)
				pass
			# for corresponding point. Finds the correct y value and draws a circle there if appropriate
			x_position = pygame.mouse.get_pos()[0]

			found_y = 1
			for idx, pt in enumerate(self.controller.curve.derivative.points):
					if abs(pt[0]-x_position) < 5:
						found_y = pt[1]
			if self.controller.curve.derivative.points[1][0]-7 <= x_position <= self.controller.curve.derivative.points[-1][0]:
				pygame.draw.circle(self.screen, (0, 0, 205), (int(x_position), int(found_y)), 4)

			elif self.controller.curve.derivative.points[-1][0] < x_position:
				pygame.draw.circle(self.screen, (0, 0, 205), (int(self.controller.curve.derivative.points[-1][0]), int(self.controller.curve.derivative.points[-1][1])), 4)

			elif self.controller.curve.derivative.points[1][0] -7 > x_position:
				pygame.draw.circle(self.screen, (0, 0, 205), (int(self.controller.curve.derivative.points[1][0]), int(self.controller.curve.derivative.points[1][1])), 4)

		#Draw the area polygons
		if self.controller.mode['Show area']:
			#initiate another surface so 
			s = pygame.Surface((1000,1000))  # the size of your rect
			s.set_alpha(100)                # alpha level
			s.fill((255,255,255))           # this fills the entire surface
			if self.controller.curve.line.area:
				for i in range(len(self.controller.curve.line.area)):
					try:
						pygame.draw.polygon(s,(0, 200, 255),self.controller.curve.line.area[i],0)
					except ValueError: #if a polygon has less than 2 points, don't draw
						pass
			self.screen.blit(s, (0,0))

			# for corresponding point. Finds the correct y value and draws a circle there if appropriate
			x_position = pygame.mouse.get_pos()[0]

			found_y = 1
			for idx, pt in enumerate(self.controller.curve.integral.points):
					if abs(pt[0]-x_position) < 5:
						found_y = pt[1]
			if self.controller.curve.integral.points[1][0]-7 <= x_position <= self.controller.curve.integral.points[-1][0]:
				pygame.draw.circle(self.screen, (0, 100, 0), (int(x_position), int(found_y)), 4)

			elif self.controller.curve.integral.points[-1][0]-7 < x_position:
				pygame.draw.circle(self.screen, (0, 100, 0), (int(self.controller.curve.integral.points[-1][0]), int(self.controller.curve.integral.points[-1][1])), 4)


		#Display critical points lines
		if self.controller.mode['Show critical points']:
			for i in self.controller.curve.derivative.cr_index:
				found_y = 1
				for idx, pt in enumerate(self.controller.curve.line.points):
					if abs(pt[0]-i[0]) < 5:
						found_y = pt[1]

				pygame.draw.line(self.screen, (204, 204, 0), (i[0],i[1]), (i[0],found_y), 2)
				

		#Display the open cv image on screen
		if self.controller.mode['Open CV drawing']:
			if self.controller.image != None:
				image=pygame.surfarray.make_surface(self.controller.image)
				image.set_alpha(150) #255 is fully opaque, 0 is fully transparent
				self.screen.blit(image,(0, 0))

		# #display the current mode 
		# self.display_text('Current mode: {}'.format(self.controller.mode),fontsmall, (186,85,211), 0,0) #purple color
		# Display the instructions for the mode underneath the mode name
		instructions = self.get_instructions_for_mode(self.controller.mode)
		self.display_text(instructions,fontsmall,(186,85,211), 0, 30)

		pygame.display.update()

	def get_instructions_for_mode(self, mode):
		if mode['Open CV drawing']:
			return 'Open CV drawing color: {}'.format(color)


		


