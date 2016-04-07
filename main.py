import pygame
import matplotlib

from mouse_control import Mouse_control
from view import View
from curve import Curve

if __name__ == "__main__":

	curve = Curve()

	view = View(curve)

	# mouse_control = Mouse_control()

	# open_cv = Open_CV_control()

	# control = Control(mouse_control, open_cv)

	# screen.fill( (255,255,255) )

	# running = True
	# while running:
	# 	pygame.time.wait(100)
	# 	# draw
while view.controller.running:

	# control.handle_event()

	view.draw_input()



	# 	mouse_control.handle_event(event)

	# 	mouse_control.print_points()

		# Open CV event
