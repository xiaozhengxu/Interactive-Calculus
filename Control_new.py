"""

"""
import pygame
import numpy as np
import argparse
import imutils
import cv2

from curve import *

greenLower=(29, 86, 6)
greenUpper=(64, 255, 255)
 
class Controller(object):
	def __init__(self):
		self.modes=[None, 'Mouse drawing','Open CV drawing', "Mouse pulling"]
		self.running_points = []
		self.running = True
		self.curve = None
		self.last_space = False
		self.last_press = False
		self.pull_point = None
		self.mode = None
		self.camera = cv2.VideoCapture(0)

	def handle_events(self):
		# print "Mode: ", self.mode
		for event in pygame.event.get():	
			if event.type == pygame.QUIT:	# Handle window closing
				self.running = False
			try:
				self.camera.release()
				cv2.destroyAllWindows()
			except:
				pass

		keys = pygame.key.get_pressed() # Returns a tuple of 1s and 0s corresponding to the the pressed keys

		if self.mode == None:
			if keys[pygame.K_SPACE] and not self.last_space: 
				self.mode = 'Open CV drawing'
				# self.open_CV = Open_CV_controller()
				self.running_points = []
				self.curve = None
				print 'Initiated open CV'

			if pygame.mouse.get_pressed()[0] and not self.last_press:
				
				if self.curve:

					mouse_pos = pygame.mouse.get_pos()

					hitbox_radius = 5

					# Find a pulling point within a hitbox
					# # Search in pull_points and points
					# for idx, pt in enumerate(self.curve.line.pull_points):
					# 	if abs(pt[0]-mouse_pos[0]) < hitbox_radius and abs(pt[1]-mouse_pos[1]) < hitbox_radius:
					# 		self.pull_point = idx
					# 		print "Pulling point is number:", idx
					# 		self.mode = 'Mouse pulling'
					# Search in points (Oh dear god the efficiency)
					for idx, pt in enumerate(self.curve.line.points):
						if abs(pt[0]-mouse_pos[0]) < hitbox_radius:
							self.pull_point = idx
							print "Pulling point is number:", idx
							self.mode = 'Mouse pulling'
				else:
					self.mode = 'Mouse drawing'
					self.running_points = []

		elif self.mode == 'Mouse drawing':

			self.draw_with_mouse()

			if pygame.mouse.get_pressed()[0] and not self.last_press: # Press Mouse1 to enter/leave Drawing mode
				self.mode = None
				print "None Mode"
				self.curve = Curve(self.running_points[::len(self.running_points)/15])  #[::len(self.running_points)/15]

		elif self.mode == 'Open CV drawing':

			self.draw_with_open_cv()

			if keys[pygame.K_SPACE] and not self.last_space:
				self.mode = None
				self.camera.release()
				cv2.destroyAllWindows()
				self.curve = Curve(self.running_points[::len(self.running_points)/15])

		elif self.mode == "Mouse pulling":
			self.pull_with_mouse()

			if pygame.mouse.get_pressed()[0] and not self.last_press: # Press Mouse1 to enter/leave Drawing mode
				self.mode = None
				print "None Mode"

		if pygame.mouse.get_pressed()[2]: # Mouse2 to clear
			self.mode = None
			self.running_points = []
			self.curve = None

		self.last_space = keys[pygame.K_SPACE] # Keep track of the last Space 
		self.last_press = pygame.mouse.get_pressed()[0]

	def draw_with_open_cv(self):
		# Grab the current frame (frame and mask are numpy.ndarray)
		print self.running_points
		(grabbed, frame) = self.camera.read()
		print grabbed
		# Resize the frame, blur it, and convert it to the HSV color space
		if grabbed:
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
						self.running_points.append((int(x),int(y)))
														# and if it doesn't curl back (last x < new x)
			cv2.imshow("Mask", hfmask)
			cv2.imshow("Horizontal flip", frame)
			cv2.waitKey(1)

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
		self.curve.line.move_point(self.pull_point, mouse_pos, kind='sigmoid')


	def print_points(self):
		print self.running_points



# if __name__ == "main":
# 	for testing
# 	mouse=Mouse_control()
# 	counter=1
# 	while counter<1000:
# 		counter+=1
# 		mouse.handle_event()

