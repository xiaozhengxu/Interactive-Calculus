"""
Handle drawing stuff to the screen
"""

import pygame
from pygame.locals import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
import numpy

import time

class View(object):
    """

    """

    def __init__(self, curve=None):
        pygame.init()
        screen = pygame.display.get_surface()

        self.screen = screen
        self.curve = curve



    def draw(self):
        fig = pylab.figure(figsize=[4, 4], # Screen Size in inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is XxY pixels
                   )
        ax = fig.gca()  # The matplotlib figure will be non-interactive
        ax.plot(self.curve.ATTRIBUTE)   #!!!
        #ax.plot([1, 2, 3, 3])   #!!!!
         
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()   # Non-interactive figures must be manually updated
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()  # The raw data (matrix) from the matplotlib graph can now be u1sed by pygame
         

        window = pygame.display.set_mode((600, 400), DOUBLEBUF) # Includes window size 
        self.screen = pygame.display.get_surface()
         
        size = canvas.get_width_height()
         
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.screen.blit(surf, (0,0))
        pygame.display.flip()

# tests = View()
# tests.draw()

