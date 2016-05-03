import pygame


#from Control import Controller
from view import View
from curve import Curve
from Model import Model

if __name__ == "__main__":


	view = View()

	while view.controller.running:

		view.draw()

