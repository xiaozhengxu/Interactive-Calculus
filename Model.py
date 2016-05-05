import pygame
import curve
import view

pygame.font.init()
fontsmall = pygame.font.SysFont('UbuntuMono',20)
fontlarge = pygame.font.SysFont('UbuntuMono',100)
fontmedium = pygame.font.SysFont('UbuntuMono',40)
fonttiny = pygame.font.SysFont('UbuntuMono', 15)

class Model(object):
	"""
	The main model class to keep track of everythg display related
	"""

	def __init__(self):
		self.grid_status = False
		self.grid_drawn = False
		self.legend_status = True
		self.buttons = {}

		button_list = ["Draw", "Clear", "Tangent", "Area", "Crit", "Grid", "Camera", "Help"]

		for label in button_list:
			self.buttons[label] = Button(label)

		# self.buttons = {
		# "Draw": Button("Draw"),
		# "Clear": Button("Clear"),
		# "Tangent": Button("Tangent"),
		# "Area": Button("Area"),
		# "Crit": Button("Crit"),
		# "Grid": Button("Grid"),
		# "Camera": Button("Camera"),
		# "Help": Button("Help")
		# }
		print self.buttons

		for i, key in enumerate(button_list): # Force the loading of buttons in an order
			self.buttons[key].position = (67 + (66+50) * i, 940)	

		# self.buttons["Tangent"].toggle = True
		# self.buttons["Area"].toggle = True	

	def grid_update(self):
		"""
		To keep track of the state of the grid
		"""
		if self.grid_status == True:
			self.grid_status = False
		elif self.grid_status == False:
			self.grid_status = True

		self.buttons["Grid"].toggle = self.grid_status

	def legend_update(self):
		if self.legend_status == True:
			self.legend_status = False
		elif self.legend_status == False:
			self.legend_status = True
		# self.legend_redraw = True


	def update(self):
		"""
		To update the model accoring to user input
		"""
		pass


class Button(object):
	"""
	Used for the modes at the bottom of the window. 
	"""

	def __init__(self, img_name, position=(-51,-51), toggle=False):
		"""
		Toggle button changes modes. 

		Attributes:
		img_name		- string: Name of image (not the path, so without "_Btn.png")
		label			- string: Label above the button in Help mode
		text_pos		- 2-tuple: Position of the label for blit
		position 		- 2-tuple: Position in Pygame window
		toggle 			- bool: Whether it is pushed in, or not
		"""

		self.position = position
		self.toggle = toggle

		self.image = pygame.image.load("Buttons/"+img_name+"_Btn.png")
		self.image.convert_alpha()

		self.background = []
		white_surf = pygame.Surface((50,50))
		grey_surf = pygame.Surface((50,50))
		white_surf.fill((255,255,255))
		grey_surf.fill((200,200,200))

		self.background.append(white_surf) 	# If toggle is False, background[toggle] is white
		self.background.append(grey_surf)	# If toggle is True, background[toggle] is grey
											# Later, this surface will be blipped before the image.

		self.label = fontsmall.render(img_name, 1, (150,150,150))
		self.text_pos = (self.position[0], 910)
		print self.label.get_width()


		


