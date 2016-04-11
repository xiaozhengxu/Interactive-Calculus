"""

"""
import pygame
from curve import *

class Controller(object):
	def __init__(self):
		self.mouse_control = Mouse_control()
		self.open_cv_control = Open_cv_control()
		self.current_control = self.mouse_control
		self.running = self.current_control.running
		self.running_points = self.current_control.running_points
		self.curve = self.current_control.curve

	def handle_events(self):
		
		self.current_control.handle_event()
		self.running = self.current_control.running
		
class Open_cv_control(object):
	def __init__(self):
		self.running_points = []
		self.mode = 'None'

	def handle_event(self,event):
		pass

class Mouse_control(object):

	def __init__(self):
		self.running_points = []
		self.curve = None
		self.running = True
		self.mode = None 
		self.last_press = False

	def handle_event(self):
		'''This method is currently called by view.draw_input()

		Allows the user to draw several lines/curves in discrete intervals with mouse. 
		Press leftbutton to start drawing, move around the mouse to draw (or hold down the lef button while drawing.
		Press leftbutton again to stop drawing. Press rightbutton to clear screen.

		running_points stores the points of the user's curve as nested lists. (if the user draws a single curve, it would be [[(x,y)...]]

		Next implementation would be to stop drawing when the leftbutton is released (MOUSEBUTTONUP doesn't work right now).'''
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			# if event.type == pygame.MOUSEBUTTONUP:
			# 	self.mode='None'
		if pygame.mouse.get_pressed()[0] and not self.last_press:
			if self.mode == 'Drawing':
				self.mode = None
				self.curve = Line(self.running_points)  #[::len(self.running_points)/15]
			else:
				self.mode = 'Drawing'

		if pygame.mouse.get_pressed()[2]:
			self.mode = 'Clear'

		if self.mode == 'Drawing':
			mouse_pos = pygame.mouse.get_pos()

			if not self.running_points:
				self.running_points.append(mouse_pos)

			if mouse_pos != self.running_points[-1]:
				self.running_points.append(mouse_pos)
				# if mouse_pos != self.running_points[-1]:
				# 	self.running_points.append(mouse_pos)
		if self.mode == 'Clear':
			self.running_points = []
		# print self.mode

		self.last_press = pygame.mouse.get_pressed()[0]

	def print_points(self):
		print self.running_points


# if __name__ == "main":
# 	for testing
# 	mouse=Mouse_control()
# 	counter=1
# 	while counter<1000:
# 		counter+=1
# 		mouse.handle_event()

