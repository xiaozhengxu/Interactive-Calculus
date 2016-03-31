"""
Handle drawing stuff to the screen
"""

import pygame
import pygame.locals import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
import numpy

class View(object):
	"""

	"""

	def __init__(self, screen, curve=None):
		self.screen = screen
		self.curve = curve

    def draw(self):


    	pygame.display.flip()


