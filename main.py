import pygame
import matplotlib

from mouse_control import Mouse_control
from view import View
from curve import Curve

if __name__ == "__main__":


	curve = Curve()


	view = View(curve)

	# control = Control(model)


while view.controller.running:

	# control.handle_event()

	view.draw_input()



	# 	mouse_control.handle_event(event)

	# 	mouse_control.print_points()

		# Open CV event
