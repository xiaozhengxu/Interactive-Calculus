import matplotlib
import numpy as np

matplotlib.use("Agg")
 
import matplotlib.backends.backend_agg as agg
 
import pylab
 
fig = pylab.figure(figsize=[4, 4], # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
ax = fig.gca()
x = np.arange(0, 5, 0.1);
y = np.sin(x)
# ax.plot([1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1])
ax.plot(x,y)
 
canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.tostring_rgb()
 
import pygame
from pygame.locals import *
 
pygame.init()
 
window = pygame.display.set_mode((600, 400), DOUBLEBUF)
screen = pygame.display.get_surface()
 
size = canvas.get_width_height()
 
surf = pygame.image.fromstring(raw_data, size, "RGB")
# screen.blit(surf, (0,0))

pygame.display.flip()

screen.fill((0,100,200))

running=True
while running:
	pygame.draw.line(screen, (255,255,255), (100,200), (300,400))
	pygame.display.update() 
	for event in pygame.event.get():
	    if event.type == QUIT:
	        running = False

