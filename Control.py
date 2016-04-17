"""

"""
import pygame
import numpy as np
# import argparse
# import imutils
# import cv2

from curve import *

greenLower=(29, 86, 6)
greenUpper=(64, 255, 255)

class Controller(object):
	def __init__(self):
		self.mouse_control = Mouse_control()
		# self.open_cv_control = Open_cv_control()
		# self.current_control = self.open_cv_control
		self.current_control = self.mouse_control	
		self.running = self.current_control.running
		self.running_points = self.current_control.running_points
		self.curve = self.current_control.curve

	def handle_events(self):
		self.current_control.handle_event()
		self.running = self.current_control.running
		self.curve = self.current_control.curve
		
class Open_cv_control(object):
	def __init__(self):
		self.running_points = []
		self.running = True
		self.curve = None
		self.last_space = False
		self.mode = 'None'
		self.camera = cv2.VideoCapture(0)
		print 'Initiated open CV'

	def handle_event(self):
		print self.mode

		for event in pygame.event.get():	
			if event.type == pygame.QUIT:	# Handle window closing
				self.running = False
				self.camera.release()
				cv2.destroyAllWindows()

		keys = pygame.key.get_pressed() # Returns a tuple of 1s and 0s corresponding to the the pressed keys

		if keys[pygame.K_SPACE] and not self.last_space: # Press space to get into or out of drawing mode
			if self.mode == 'None':
				self.mode = 'Drawing'
			elif self.mode =='Drawing':
				self.mode = 'None'
				self.camera.release()
				cv2.destroyAllWindows()
				self.curve = Curve(self.running_points[::len(self.running_points)/15])

		self.last_space = keys[pygame.K_SPACE] # Keep track of the last Space 

		# Grab the current frame (frame and masl are numpy.ndarray)
		if self.mode == 'Drawing':
			print self.running_points
			(grabbed, frame) = self.camera.read()

			# Resize the frame, blur it, and convert it to the HSV color space
			frame = imutils.resize(frame, width=600)
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

			# Construct a mask for the color "green", then perform a series of dilations and erosions to remove any small
			# blobs left in the mask
			mask = cv2.inRange(hsv, greenLower, greenUpper)
			mask = cv2.erode(mask, None, iterations=2)
			mask = cv2.dilate(mask, None, iterations=2)

			# Flip the mask and frame horizontally
			hfmask = cv2.flip(mask,1)
			hfframe = cv2.flip(frame,1)

			# Find contours in the mask and initialize the current
			# (x, y) center of the ball
			cnts = cv2.findContours(hfmask.copy(), cv2.RETR_CCOMP,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
			center = None

			# Only proceed if at least one contour was found
			if len(cnts) > 0:
				# Find the largest contour in the mask, then use
				# it to compute the minimum enclosing circle and
				# centroid
				c = max(cnts, key=cv2.contourArea)
				((x, y), radius) = cv2.minEnclosingCircle(c)

				# Only proceed if the radius meets a minimum size
				if radius > 30:
					pts=(int(x),int(y))

					cv2.circle(hfframe, pts, int(radius),(0, 255, 255), 2)

					if not self.running_points:
						self.running_points.append(pts)

					if pts != self.running_points[-1] and self.running_points[-1][0] < pts[0]: 	# Add point if it is different than the previous
						self.running_points.append((int(x),int(y)))								# and if it doesn't curl back (last x < new x)
			# cv2.imshow("Mask", hfmask)
			cv2.imshow("Horizontal flip", frame)

		
class Mouse_control(object):

	def __init__(self):
		self.running_points = []
		self.curve = None
		self.running = True
		self.mode = None 
		self.last_press = False

	def handle_event(self):
		'''This method is currently called by view.draw_input()

		Allows the user to draw several lines/curves in discrete intervals with mouse. 
		Press leftbutton to start drawing, move around the mouse to draw (or hold down the lef button while drawing.
		Press leftbutton again to stop drawing. Press rightbutton to clear screen.

		running_points stores the points of the user's curve as nested lists. (if the user draws a single curve, it would be [[(x,y)...]]

		Next implementation would be to stop drawing when the leftbutton is released (MOUSEBUTTONUP doesn't work right now).'''
		for event in pygame.event.get(): # Check for game quit
			if event.type == pygame.QUIT:
				self.running = False

		if pygame.mouse.get_pressed()[0] and not self.last_press: # Press Mouse1 to enter/leave Drawing mode
			if self.mode == 'Drawing':
				self.mode = None
				print "None Mode"
				self.curve = Curve(self.running_points[::len(self.running_points)/15])  #[::len(self.running_points)/15]
				# print self.curve
			else:
				print "Drawing mode"
				self.mode = 'Drawing'

		if pygame.mouse.get_pressed()[2]: # Mouse2 to clear
			print "Clear Mode"
			self.mode = 'Clear'

		if self.mode == 'Drawing':
			mouse_pos = pygame.mouse.get_pos()

			# Add points based off of mouse position
			if not self.running_points:
				self.running_points.append(mouse_pos)

			if mouse_pos != self.running_points[-1] and self.running_points[-1][0] < mouse_pos[0]: # NOTE: This is where we check if the user goes backwards
				self.running_points.append(mouse_pos)

		if self.mode == 'Clear':
			self.running_points = []	# Delete all of the curves
			self.curve = None
			self.mode = None
		# print self.mode

		self.last_press = pygame.mouse.get_pressed()[0]

	def print_points(self):
		print self.running_points

# '''This method is currently called by view.draw_input()

# 		Allows the user to draw several lines/curves in discrete intervals with mouse. 
# 		Press leftbutton to start drawing, move around the mouse to draw (or hold down the lef button while drawing.
# 		Press leftbutton again to stop drawing. Press rightbutton to clear screen.

# 		running_points stores the points of the user's curve as nested lists. (if the user draws a single curve, it would be [[(x,y)...]]

# 		Next implementation would be to stop drawing when the leftbutton is released (MOUSEBUTTONUP doesn't work right now).'''


# if __name__ == "main":
# 	for testing
# 	mouse=Mouse_control()
# 	counter=1
# 	while counter<1000:
# 		counter+=1
# 		mouse.handle_event()

