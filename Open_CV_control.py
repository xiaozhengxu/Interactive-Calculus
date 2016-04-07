""" return a curve input using OpenCV """

import cv2
import numpy as np
import time 
#Boundaries that specify the colors of a boundary. 

class Open_CV_control(object):

	def __init__(self):
		self.running_points = []

	def handle_event(self, event):
		cap=cv2.VideoCapture(0)
	    # Take each frame
	    _, frame = cap.read()

	    # define range of red color in BGR 
	    lower_red = np.array([0, 0, 120], dtype = "uint8")
	    upper_red = np.array([80, 80, 255], dtype = "uint8")

	    # Threshold the HSV image to get only blue colors
	    mask = cv2.inRange(frame, lower_red, upper_red)

	    print 'Mask is of shape', mask.shape

	    marker_pos=np.where(mask==255) #Marker_pos is a array of 

	    print 'mask has a red pixels', np.where(mask == 255)


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()