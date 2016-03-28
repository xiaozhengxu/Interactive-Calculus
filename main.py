import pygame
import matplotlib

from mouse_control import Mouse_control
from view import View

if __name__ == "__main__":
	screen_size = (640, 480)


	pygame.init()
	screen = pygame.display.set_mode(screen_size)
	mouse_control = Mouse_control()

	screen.fill( (255,255,255) )

	running = True
	while running:
		pygame.time.wait(100)
		# draw
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			mouse_control.handle_event(event)

			mouse_control.print_points()

			prev_event = event

			# Open CV event
