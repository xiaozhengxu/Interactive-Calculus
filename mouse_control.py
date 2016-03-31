"""

"""
import pygame

class Mouse_control(object):

	def __init__(self):
		self.running_points = []

	def handle_event(self, event):

		if event.type == pygame.MOUSEBUTTONDOWN:
			self.running_points = []

		if pygame.mouse.get_pressed()[0]:
			mouse_pos = pygame.mouse.get_pos()

			if not self.running_points:
				self.running_points.append(mouse_pos)

			if mouse_pos != self.running_points[-1]:
				self.running_points.append(mouse_pos)

	def print_points(self):
		print self.running_points


