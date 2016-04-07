"""

"""
import pygame


class Mouse_control(object):

	def __init__(self):
		self.running_points = []
		self.running=True
		self.mode = 'None'

	def handle_event(self):
		'''This method is currently called by view.draw_input()

		Allows the user to draw several lines/curves in discrete intervals with mouse. 
		Press leftbutton to start drawing, move around the mouse to draw (or hold down the lef button while drawing.
		Press leftbutton again to stop drawing. Press rightbutton to clear screen.

		running_points stores the points of the user's curve as nested lists. (if the user draws a single curve, it would be [[(x,y)...]]

		Next implementation would be to stop drawing when the leftbutton is released (MOUSEBUTTONUP doesn't work right now.'''

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			# if event.type == pygame.MOUSEBUTTONUP:
			# 	self.mode='None'

		if pygame.mouse.get_pressed()[0]:
			if self.mode=='Drawing':
				self.mode='None'
			else:
				self.mode='Drawing'
				self.running_points.append([])

		if pygame.mouse.get_pressed()[2]:
			self.mode ='Clear'

		if self.mode=='Drawing':
			mouse_pos = pygame.mouse.get_pos()

			if not self.running_points[-1]:
				self.running_points[-1].append(mouse_pos)

			if mouse_pos != self.running_points[-1][-1]:
				self.running_points[-1].append(mouse_pos)
				# if mouse_pos != self.running_points[-1]:
				# 	self.running_points.append(mouse_pos)
		if self.mode=='Clear':
			self.running_points=[]
		# print self.mode

	def print_points(self):
		print self.running_points

#for testing
# mouse=Mouse_control()
# counter=1
# while counter<1000:
# 	counter+=1
# 	mouse.handle_event()

