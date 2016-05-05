"""

"""
import pygame
import numpy as np

try:
	import argparse
	import imutils
	import cv2
except:
	print "Open CV libraries not loaded."


from curve import *
from Model import *

#define HSV color range of a tennis ball: open cv has range: H: 0-180, S: 0 -255, V: 0-255
colors = {'bright_green':[(29, 84, 6),(64, 255, 255)],'bright_pink':[(145,84,120),(175,255,255)]}
color = 'bright_pink' # Used for OpenCV

class Controller(object): 
	"""
	Handles Keyboard, Mouse and OpenCV inputs. 
	Instantiated in view.py. 

	Attributes: 
	running_points 		- Array holding points as they are drawn, but before a curve is created.
	running 			- Bool telling main.py if the game is running (ie when it stops).
	curve 				- Curve object, encapsulating the input line, the derivative and integral.
	last 				- Dictionary of the previous status of relavent keys last loop.
	pull_point 			- Index of the point being pulled when moving with Handles.
	mode 				- Dictionary with the mode for key, and a bool indicating whether it is active for value.
	model 				- Model object.
	pull_mode			- String, either Handle or Curve. 
	image 				- Image used by OpenCV.

	Methods:
	handle_events		- Handles all events (run at every loop iteration).
	change_mode			- Change mode based on keypresses.
	draw_with_mouse 	- Get mouse input and add to running_points. Makes sure that the x values are monotonically increasing.
	pull_with_mouse 	- Logic behind moving a curve from mouse input.
	find_curve			- Hitbox handling when finding a handle on a curve.
	"""
	def __init__(self):
		self.modes=[None, 'Mouse drawing','Open CV drawing', "Mouse pulling", 'Open CV calibrating','Show tangent', 'Show area', 'Show critical points']

		try:
			self.open_cv_control = Open_cv_control()
		except:
			pass

		self.running_points = [] 	# Used for recording points
		self.running = True			# Used by main to check if the code quits
		self.curve = None		

		self.last = { 				# Used to get key press 
		"space": False,
		"press": False,
		"g": False,
		"l": False,
		"w": False,
		"a": False,
		"c": False,
		"h": False
		}

		self.mode = {
		"Show tangent": False,
		"Show area": False,
		"Show critical points": False,
		"Mouse drawing": False,
		"Mouse pulling": False,
		"Open CV drawing": False,
		"Open CV calibrating": False,
		"Show help": False
		}

		self.pull_point = None		# Determing which point is being pulled

		self.model = Model()

		self.pull_mode = "Handle"
		self.image = None


	def handle_events(self):
		"""
		Handles all events. Called by view.draw(). 
		"""

		# Check for quitting the game
		for event in pygame.event.get():	
			if event.type == pygame.QUIT:	# Handle window closing
				try: 
					self.open_cv_control.close_camera()
				except:
					print "OpenCV not loaded, no camera to close"
				self.running = False

		keys = pygame.key.get_pressed() # Returns a tuple of 1s and 0s corresponding to the the pressed keys
		
		hitbox_radius = 5 # Hitbox for clicking on curves


		# Perform the mode's action
		if self.mode['Mouse drawing']:

			self.draw_with_mouse()

			if pygame.mouse.get_pressed()[0] and not self.last["press"]: # Press Mouse1 to enter/leave Drawing mode
				self.clear_modes()
				if len(self.running_points)>15:
					self.curve = Curve(self.running_points[::len(self.running_points)/7], self.pull_mode)  #[::len(self.running_points)/15]
				else:
					print 'Not enough points registered'

		elif self.mode['Open CV calibrating']:
			self.open_cv_control.calibrate_color()
			if keys[pygame.K_c] and not self.last["w"]:
				self.clear_modes()

		elif self.mode['Open CV drawing']:
			try:
				self.open_cv_control.draw_with_open_cv()
			except:
				pass
			self.image = self.open_cv_control.image

			self.running_points = self.open_cv_control.running_points

			if keys[pygame.K_SPACE] and not self.last["space"]:
				self.clear_modes()
				if len(self.running_points)>15:
					self.curve = Curve(self.running_points[::len(self.running_points)/15], self.pull_mode)  
					print self.running_points
				else:
					print 'Not enough points registered'

		elif self.mode["Mouse pulling"]:
			self.pull_with_mouse()
		
		if self.mode["Show tangent"]:
			idx = self.find_point(self.curve.line.points, vertical=False)
			if idx != None:
				self.tangent_point = idx
				self.curve.line.make_tangent(self.tangent_point,200)

		if self.mode['Show area']:
			idx = self.find_point(self.curve.line.points, vertical=False)
			if idx != None:
				self.curve.line.make_area(idx) 

		if self.mode["Show critical points"]:

			if self.curve:
				self.curve.derivative.make_crpoints()

		# Change self.mode according to keypresses
		self.change_mode_key(keys)

		# Change self.mode according to on-screen buttons
		if pygame.mouse.get_pressed()[0] and not self.last["press"]:
			self.change_mode_btn()

		# Update the button's model of the current mode
		self.update_buttons()

		# Stuff to change grid, legend etc.
		if keys[pygame.K_g] and not self.last["g"]:
			self.model.grid_update()
		if keys[pygame.K_l] and not self.last["l"]:
			self.model.legend_update()
		if keys[pygame.K_h] and not self.last["h"]:
			self.model.legend_update()

		# Keep track of last key presses
		self.last["space"] = keys[pygame.K_SPACE] 
		self.last["press"] = pygame.mouse.get_pressed()[0]
		self.last["g"] = keys[pygame.K_g]
		self.last["l"] = keys[pygame.K_l]
		self.last["w"] = keys[pygame.K_c]
		self.last["t"] = keys[pygame.K_t]
		self.last["a"] = keys[pygame.K_a]
		self.last["c"] = keys[pygame.K_c]
		self.last["h"] = keys[pygame.K_h]

	def change_mode_key(self, keys):
		"""
		Check if the user is changing modes.
		Used in self.handle_events()
		"""

		# Moving handles and creating Curve
		if pygame.mouse.get_pressed()[0] and not self.last["press"]:
			if self.mode["Mouse pulling"]: 	# Leave pulling mode if in drawing mode
				self.mode["Mouse pulling"] = False

			elif self.curve:				# If there is already a curve, find a pull point and get into pulling mode
				if self.pull_mode == "Handle":
					self.pull_point = self.find_point(self.curve.line.pull_points)

				elif self.pull_mode == "Curve":
					self.pull_point = self.find_point(self.curve.line.points, vertical=True)

				if self.pull_point != None:
					print "Pulling point is number:", self.pull_point
					self.mode['Mouse pulling'] = True
			else:
				self.clear_modes()
				self.mode['Mouse drawing'] = True
				self.running_points = []

		# Clearing the screen if mouse 2 is pressed
		if pygame.mouse.get_pressed()[2]: # Mouse2 to clear
			self.clear_screen()

		# Open CV Drawing
		if keys[pygame.K_SPACE] and not self.last["space"]: 
			if self.mode['Open CV drawing']:
				self.mode['Open CV drawing'] = False
			else:
				self.mode['Open CV drawing'] = True
				self.open_cv_control.running_points = []
				self.running_points = []
				self.curve = None

		# Tangent
		if keys[pygame.K_t] and not self.last["t"]:
			if self.mode["Show tangent"]:
				self.mode["Show tangent"] = False
			elif self.curve:
				self.mode["Show tangent"] = True

		# Area
		if keys[pygame.K_a] and not self.last["a"]:
			if self.mode["Show area"]:
				self.mode["Show area"] = False
			elif self.curve:
				self.mode["Show area"] = True

		# Critical points
		if keys[pygame.K_c] and not self.last["c"]:

			if self.mode["Show critical points"]:
				self.mode["Show critical points"] = False
			elif self.curve:
				self.mode["Show critical points"] = True

	def update_buttons(self):
		"""
		Update the toggle attribute of the buttons based on the modes.
		"""
		self.model.buttons["Draw"].toggle = self.mode["Mouse drawing"]
		self.model.buttons["Camera"].toggle = self.mode["Open CV drawing"]
		self.model.buttons["Tangent"].toggle = self.mode["Show tangent"]
		self.model.buttons["Area"].toggle = self.mode["Show area"]
		self.model.buttons["Crit"].toggle = self.mode["Show critical points"]

	def change_mode_btn(self):
		"""
		Change the various modes based on button clicks.
		"""
		if self.button_hit("Draw") and not self.curve:

			self.clear_modes()				# Get into Drawing mode
			self.mode['Mouse drawing'] = True
			self.running_points = []

		elif self.button_hit("Clear"):
			self.clear_screen()

		elif self.button_hit("Camera"):
			if self.mode['Open CV drawing']:
				self.mode['Open CV drawing'] = False
			else:
				try:
					self.open_cv_control.running_points = []
					self.mode['Open CV drawing'] = True
					self.running_points = []
					self.curve = None
				except:
					print "Open CV Not available."

		elif self.button_hit("Tangent"):
			if self.mode["Show tangent"]:
				self.mode["Show tangent"] = False
			elif self.curve:
				self.mode["Show tangent"] = True

		elif self.button_hit("Area"):
			if self.mode["Show area"]:
				self.mode["Show area"] = False
			elif self.curve:
				self.mode["Show area"] = True

		elif self.button_hit("Crit"):
			if self.mode["Show critical points"]:
				self.mode["Show critical points"] = False
			elif self.curve:
				self.mode["Show critical points"] = True

		elif self.button_hit("Grid"):
			self.model.grid_update()

		elif self.button_hit("Help"):
			self.mode["Show help"] = not self.mode["Show help"]


	def button_hit(self, button_key):
		"""
		Determines if the mouse is in the button's hitbox. Returns appropriate bool.
		"""
		mouse = pygame.mouse.get_pos()
		pos = self.model.buttons[button_key].position
		if pos[0] <= mouse[0] and mouse[0] <= pos[0]+50: # Check x component
			if pos[1] <= mouse[1] and mouse[1] <= pos[1]+50:
				return True
		return False


	def clear_modes(self):
		"""
		Makes the value for all modes False. 
		Used when there should only be one mode
		"""
		print "Clearing Mode"
		for key in self.mode:
			self.mode[key] = False

	def draw_with_mouse(self):
		'''This method is currently called by view.draw_input()

		Allows the user to draw several lines/curves in discrete intervals with mouse. 
		Press leftbutton to start drawing, move around the mouse to draw (or hold down the lef button while drawing.
		Press leftbutton again to stop drawing. Press rightbutton to clear screen.

		running_points stores the points of the user's curve as nested lists. (if the user draws a single curve, it would be [[(x,y)...]]

		Next implementation would be to stop drawing when the leftbutton is released (MOUSEBUTTONUP doesn't work right now).'''

		mouse_pos = pygame.mouse.get_pos()
		# Add points based off of mouse position
		if not self.running_points:
			self.running_points.append(mouse_pos)

		if mouse_pos != self.running_points[-1] and self.running_points[-1][0] < mouse_pos[0]: # NOTE: This is where we check if the user goes backwards
			self.running_points.append(mouse_pos)

	def pull_with_mouse(self):
		# Get new mouse positions
		mouse_pos = pygame.mouse.get_pos()
		# Move point there
		self.curve.move_point(self.pull_point, mouse_pos, line="line")

	def clear_screen(self):
		"""
		Clears the curves.
		"""
		self.clear_modes()
		self.running_points = []
		try:
			self.open_cv_control.running_points = []
		except:
			print "OpenCV not loaded, Cannot reset open_cv_control.running_points "
		self.curve = None


	def find_point(self, all_points, vertical=True, radius=5):
		"""
		Find a point from a mouse click on a list of points.
		vertical is a bool; when False it disables vertical search (you can select a point by clicking under it)
		"""
		mouse = pygame.mouse.get_pos()

		found_idx = None
		for idx, pt in enumerate(all_points):
			if abs(pt[0]-mouse[0]) < radius and (abs(pt[1]-mouse[1]) < radius or not vertical):
				found_idx = idx
		return found_idx

class Open_cv_control(object):
	def __init__(self):
		self.running_points = []
		self.camera = cv2.VideoCapture(0)
		self.camera.set(3,640) #setting camera size
		self.camera.set(4,480) #setting camera size
		self.prev_avg_col = (0,0,0)
		self.color = color
		self.draw_color_lower = colors[self.color][0]
		self.draw_color_upper = colors[self.color][1]
		self.image = None
		print 'Initiated open CV'

	def draw_with_open_cv(self):
		# Grab the current frame (frame and masl are numpy.ndarray)
		(grabbed, frame) = self.camera.read()
		if grabbed:
			# Resize the frame, blur it, and convert it to the HSV color space
			frame = imutils.resize(frame, width=600)
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

			# Construct a mask for the color "green", then perform a series of dilations and erosions to remove any small
			# blobs left in the mask
			mask = cv2.inRange(hsv, self.draw_color_lower, self.draw_color_upper)
			mask = cv2.erode(mask, None, iterations=2)
			mask = cv2.dilate(mask, None, iterations=2)

			# Flip the mask and frame horizontally so it's the direction of draw
			hfmask = cv2.flip(mask,1)
			hfframe = cv2.flip(frame,1) #flip if use open cv to display image

			# Find contours in the mask and initialize the current
			# (x, y) center of the balls
			cnts = cv2.findContours(hfmask.copy(), cv2.RETR_CCOMP,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
			center = None
		# Only proceed if at least one contour was found
			if len(cnts) > 0:
				# Find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
				c = max(cnts, key=cv2.contourArea)
				((x, y), radius) = cv2.minEnclosingCircle(c)

				# Only proceed if the radius meets a minimum size
				if radius > 30:
					pts=(int(x),int(y))

					cv2.circle(hfframe, pts, int(radius),(0, 255, 255), 2)

					if not self.running_points:
						print 'appending points'
						self.running_points.append(pts)

					if pts != self.running_points[-1] and self.running_points[-1][0] < pts[0]: 	# Add point if it is different than the previous
						print 'appending points'
						self.running_points.append(pts)								# and if it doesn't curl back (last x < new x)
			
			for i in xrange(1, len(self.running_points)):
				# if either of the tracked points are None, ignore them
				if self.running_points[i - 1] is None or self.running_points[i] is None:
					continue
				# otherwise, compute the thickness of the line and draw the connecting lines
				thickness = 2
				cv2.line(hfframe, self.running_points[i - 1], self.running_points[i], (255, 0, 0), thickness)
			
			#Set self.image to frame to display in pygame window
			self.image = cv2.cvtColor(hfframe,cv2.COLOR_BGR2RGB)
			self.image = cv2.flip(self.image,1) #flip the image back for pygame display and rotate the image 
			self.image = np.rot90(self.image) 


			#Uncomment the following lines to show frame and mask
			# cv2.imshow("Mask", hfmask)
			# cv2.imshow("Horizontal flip", hfframe)
			cv2.waitKey(1)  #waitKey displays each image for 1 ms. and allow the loop to run. if itt's 0 the image will be displayed infinitely and no input will be accepted
			

	def calibrate_color(self):
		(grabbed, frame) = self.camera.read()
		if grabbed:
			frame_size = frame.shape
			frame_ct = (frame_size[1]/2,frame_size[0]/2)
			print frame[frame_ct[0],frame_ct[1]]
			cv2.circle(frame, frame_ct, 20,(142, 37, 149), -1) #bright pink color

			cv2.rectangle(frame, (frame_ct[0]-50,frame_ct[1]-50),(frame_ct[0]+50,frame_ct[1]+50), (0,255,255),2)
			cv2.imshow('Frame',frame)
			cv2.waitKey(1)


	def close_camera(self):
		self.camera.release()
		cv2.destroyAllWindows()
