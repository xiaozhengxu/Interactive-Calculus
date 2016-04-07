import numpy as np
import argparse
import cv2


cap=cv2.VideoCapture(0)
running_points = []

while (1):
    # Take each frame
    _, frame = cap.read()
    #frame is of size 480, 640

    # define range of red color in BGR 
    lower_red = np.array([0, 0, 120], dtype = "uint8")
    upper_red = np.array([80, 80, 255], dtype = "uint8")

    # Threshold the HSV image to get only red color
    mask = cv2.inRange(frame, lower_red, upper_red)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    marker_pos=np.where(mask==255)
    x_marker_pos=marker_pos[0] 
    y_marker_pos=marker_pos[1]
    
    if len(x_marker_pos)>0:
	    len_marker_pos=len(x_marker_pos)
	    print 'mask has a red pixels', x_marker_pos[len_marker_pos/2], y_marker_pos[len_marker_pos/2]
	    running_points.append((x_marker_pos[len_marker_pos/2], y_marker_pos[len_marker_pos/2]))

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
		break
print(running_points)

cap.release()
cv2.destroyAllWindows()

# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "-/image.png", help = "path to the image")
# args = vars(ap.parse_args())
 
# # load the image
# image = cv2.imread(args["image.png"])

# # define the list of boundaries
# boundaries = [
# 	([17, 15, 100], [50, 56, 200]),
# 	([86, 31, 4], [220, 88, 50]),
# 	([25, 146, 190], [62, 174, 250]),
# 	([103, 86, 65], [145, 133, 128])
# ]

# # loop over the boundaries
# for (lower, upper) in boundaries:
# 	# create NumPy arrays from the boundaries
# 	lower = np.array(lower, dtype = "uint8")
# 	upper = np.array(upper, dtype = "uint8")
 
# 	# find the colors within the specified boundaries and apply
# 	# the mask
# 	mask = cv2.inRange(image, lower, upper)
# 	output = cv2.bitwise_and(image, image, mask = mask)
 
# 	# show the images
# 	cv2.imshow("images", np.hstack([image, output]))
# 	cv2.waitKey(0)
