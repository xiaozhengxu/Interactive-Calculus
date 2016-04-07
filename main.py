import pygame
import matplotlib

from mouse_control import Mouse_control
from view import View
from curve import Curve

if __name__ == "__main__":

	model = Curve()

	view = View(curve)

	control = Control(model)

	

    while control.running:
    	control.handle_event()

        view.update()
