import pygame
import matplotlib

from Control_new import Controller
from view import View
from curve import Curve

if __name__ == "__main__":

	view = View()
	view.draw_graph(grid=True)

while view.controller.running:

	view.draw_input()

	# 	mouse_control.handle_event(event)

	# 	mouse_control.print_points()

		# Open CV event
