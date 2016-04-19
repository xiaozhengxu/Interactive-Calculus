import pygame
import matplotlib

from Control_new import Controller
from view import View
from curve import Curve

if __name__ == "__main__":

	view = View()

while view.controller.running:

	view.draw()

