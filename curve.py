from scipy import interpolate
import numpy as np
import math

def trap(a, b):
	"""
	Take points a, b which are (x,y) tuples, and find the trapezoidal area.
	"""
	dx = b[0]-a[0]
	return (a[1]+b[1])*dx/2.0

class Curve(object):
	"""
	Takes in an of tuples. Curve creates three Line objects which are the input line, derivative of that line and integral of the same. These are initialized in the init. 
	Curve has a method move_point which allows the user to click and drag graphed lines, seeing how the line, derivative and integral change. 

	"""

	def __init__(self, points, pull_mode):
		"""
		Initializes the input points as a Line and finds the corresponding derivative and integral through methods of Line. Input points must be smoothed.
		The derivative and integral of a smooth line will be smooth without smoothening.
		"""
		self.pull_mode = pull_mode
		self.line = Line(points, pull_mode=self.pull_mode)
		self.derivative = Line(self.line.derive(), smooth_bool=True, pull_mode=self.pull_mode)
		self.integral = Line(self.line.integrate(), smooth_bool=True, pull_mode=self.pull_mode)

	def move_point(self, handle, new_pos, line='line'):
		"""
		This method adjusts the three related lines as the user clicks and drags points on one of them. If the input line is changed, the derivative and integral
		are changed. If the derivative is changed, the line and integral are changed. In this case the new line is found through integrating the changed derivative.
		A similar process happens if the integral is changed.
		This function is called by pull_with_mouse() in Control.py: self.curve.move_point(self.pull_point, mouse_pos, line="line")
		"""
		if line == 'line':
			self.line.move_point(handle, new_pos, kind="sigmoid")
			if self.pull_mode == "Handle":
				pass
				# Re-interpolate the line through the moved handle points
				self.line = Line(self.line.pull_points, keep_points=True)

			self.derivative = Line(self.line.derive(), smooth_bool=True, pull_mode=self.pull_mode)
			self.integral = Line(self.line.integrate(), smooth_bool=True, pull_mode=self.pull_mode)

		elif line == 'derivative':
			self.derivative.move_point(handle, new_pos, kind="sigmoid")

			self.line = Line(self.derivative.integrate(), smooth_bool=True, pull_mode=self.pull_mode) # The new line will be the integral of the changed derivative
			self.integral = Line(self.line.integrate(), smooth_bool=True, pull_mode=self.pull_mode)   # Back to normal

		elif line == 'integral':
			self.integral.move_point(handle, new_pos, kind="sigmoid")

			self.line = Line(self.integral.derive(), smooth_bool=True, pull_mode=self.pull_mode) # The new line will be the derivative of the changed integral
			self.derivative = Line(self.line.derive(), smooth_bool=True, pull_mode=self.pull_mode)    # Back to normal

	def draw_to_plot(self, variables=['line', 'derivative', 'integral']):
		"""
		This method is for testing purposes. It plots the line, integral and derivative in matplotlib.
		"""

		if any(var == 'line' for var in variables):
			# print 'Plotting line'
			# print self.line.points
			xy_s = zip(*self.line.points)
			# print xy_s[1]
			plt.plot(xy_s[0], xy_s[1], 'r-')

		if any(var == 'derivative' for var in variables):
			# print 'Plotting derivative'
			pts = [(pt[0], pt[1]) for pt in self.derivative.points]
			xy_d = zip(*pts)
			print xy_d[1]
			plt.plot(xy_d[0], xy_d[1], 'g-')

		if any(var == 'integral' for var in variables):
			# print 'Plotting integral'
			xy_i = zip(*self.integral.points)
			# print xy_i[1]
			# print xy_i[1][10]
			plt.plot(xy_i[0], xy_i[1], 'b-')

		plt.show()

class Line(object):
	"""
	A class that takes in list of points. Contains attributes to smooth, derive, integrate, and adjust itself.
	"""

	def __init__(self, points, pull_pts_num=7, smooth_bool=False, keep_points=False, pull_mode="Handle"):  
		"""
		Initializes a line class. If the line is not considered smooth, the smoothen() method is called.
		""" 
		# print "Making Line"
		self.pull_mode = pull_mode
		if smooth_bool:     # If the points are smooth, don't bother smoothening the curve
			self.points = points
			# print len(points)
			self.pull_points = (0,0)  
			#points[::len(points)/pull_pts_num]
		else:
			if keep_points:
				self.points = self.smoothen(points, pull_pts_num=pull_pts_num)[0]
				self.pull_points = points
			else:
				self.points, self.pull_points = self.smoothen(points, pull_pts_num=pull_pts_num)

		self.tangent = None
		self.area = None
	
	def __index__(self, idx):
		"""
		Method that allows index of Line to be called. Ex: Line[index] will work as if Line was a list. 
		"""
		return self.points[idx]

	def make_tangent(self,idx,tangent_length):
		'''This function gets the derivative at a point and returns a tangent array containing two points to be plotted'''
		x = self.points[idx][0]
		y = self.points[idx][1]
		x_prev = self.points[idx-1][0]
		y_prev = self.points[idx-1][1]
		
		dx = x-x_prev 
		dy = y-y_prev 
		slope = dy/dx

		c_x = np.sqrt((tangent_length/2)**2/(1+slope**2))	# This equation was found with c_x^2+c_y^2=(tangent_length/2)^2 and c_y=c_x*slope
		c_y = slope*c_x
		self.tangent = [(x+c_x,y+c_y),(x-c_x,y-c_y)]

	def make_area(self,idx):
		'''This function gets a user input point and creates a list of lists of points to be plotted by view with pygame.draw.polygon'''

		polygon = [[]]
		prev_pt = self.points[0]
		polygon_num = 0
		polygon[polygon_num].append((self.points[0][0],500))
		for i,pt in enumerate(self.points[:idx]):
			if (pt[1]-500)*(prev_pt[1]-500)>0:
				polygon[polygon_num].append(pt)

			elif (pt[1]-500)*(prev_pt[1]-500)<0:
				polygon[polygon_num].append((self.points[i-1][0],500))
				polygon.append([])
				polygon_num+=1
				#Add the point on the x axis
				polygon[polygon_num].append((self.points[i-1][0],500))
			prev_pt = pt

		polygon[polygon_num].append((self.points[idx][0],500))
		# print polygon
		print 'there are {} polygons'.format(len(polygon))
		self.area = polygon

	def deep_copy(self):
		"""
		Method that allows a Line object to be copied. 
		"""
		return Line(self.points[:])

	def smoothen(self, points, pull_pts_num=3):
		"""
		Smooths input points. Since user drawn points may not be smooth, this method smooths them using scipy's interpolation.
		"""
		unzip = zip(*points)    # unzip the (x,y) tuples into a list of x and a list of y
		x = unzip[0]
		y = unzip[1]

		interpol = interpolate.interp1d(x,y, kind='cubic')  # Magic interpolation

		# num_points = (x[-1] - x[0])
		num_points = 100

		xnew = np.linspace(x[0]+1, x[-1]-1, num_points) # Smooth Line
		ynew = interpol(xnew)

		xpull = np.linspace(x[0]+1, x[-1]-1, pull_pts_num)  # Pulling Points
		ypull = interpol(xpull)

		return (zip(xnew, ynew), zip(xpull, ypull))         # zip the list of x and list of y into (x,y) tuples

	def move_point(self, index, new_pos, kind='relative'): # currently doesn't change the local Line
		"""
		Method to adjust the points of a line as it is adjusted/dragged through user input. 
		A line is adjusted when the user pulls its "pulling points". 
		called by move_point in curve: self.line.move_point(handle, new_pos, kind="sigmoid")
		"""
		if self.pull_mode == "Curve":    
			pts = self.points   #Because self.points is a list, modifying pts changes the original self.points 
		elif self.pull_mode == "Handle":
			pts = self.pull_points
			kind = None

		distance_x = float(new_pos[0] - pts[index][0])    # Distance pulling point moved
		distance_y = float(new_pos[1] - pts[index][1])    # Distance pulling point moved

		if index >= len(pts):
			print 'Index out of Range'
			return None

		if kind == 'absolute':
			factor = 1.5
			# Absolute change in Distance 					# NOTE: Smoother curve moving
			for i, pt in enumerate(pts[:index]):
				pts[i] = (pts[i][0], pts[i][1] + distance_y / (index-i+1)**0.7)
				print 'moved', distance_y / (index-i+1)

			for i, pt, in enumerate(pts[index:]):
				pts[i+index] = (pts[i+index][0], pts[i+index][1] + distance_y / (i+1)**0.7)
				print 'moved', distance_y / (i+1)

		elif kind == 'sigmoid':  #This is the one we're using right now. 
			sigmoid_size = 1/3
			S = lambda d: 1/(1+math.exp(d/2.0-4)) # Sigmoid function

			for i, pt in enumerate(pts):
				pts[i] = (pts[i][0], pts[i][1] + distance_y * (S(abs(index-i))+1-S(0)))

		elif kind == 'pull point':
			p_pts = self.pull_points
			S = lambda d: 1/(1+math.exp^(2*x-4)) # Sigmoid function

			for i, pt in enumerate(pts):
				p_pts[i] = (p_pts[i][0], p_pts[i][1] + distance_y * (S(abs(index-i))+1-S(0)))

		elif kind == 'relative':
			rel_d = distance_y / pts[index][1] 
			for i, pt in enumerate(pts[:index]):
				pts[i] = (pts[i][0], pts[i][1] * (1 + (rel_d / (index-i+1))))   # For the line to the left of the adjusted point, shift each value accordintly. The adjustment becomes larger, closer to the point that was adjusted.
				# print 'moved', 1 + rel_d / (index-i+1)

			for i, pt, in enumerate(pts[index:]):
				pts[i+index] = (pts[i+index][0], pts[i+index][1] * (1 + (rel_d / (i+1))))   # Similar to above
				# print 'moved', 1 + rel_d / (i+1)
		elif kind == None:
			# # Only move the selected point (used when moving handles)
			# pts[index] = (new_pos[0], new_pos[1]) # TODO: Keep points in order
			space = 3

			first_point = index == 0 and (new_pos[0] < pts[index+1][0]-space)
			last_point = pts[index] == pts[-1] and (pts[index-1][0]+space < new_pos[0])
			other_point = False
			if not first_point and not last_point:
				other_point = pts[index-1][0]+space < new_pos[0] and new_pos[0] < pts[index+1][0]-space

			if first_point or last_point or other_point:
				pts[index] = (new_pos[0], new_pos[1])
			else:
				pts[index] = (pts[index][0], new_pos[1])


		else:
			print 'Invalid Version'
			return None
	
	def derive(self):
		"""
		Method that creates a list of tuples which is the derivative of the current Line object.
		"""
		deriv = []
		prev_pt = self.points[0]

		for pt in self.points[1:]:
			deriv.append( ((pt[0]+prev_pt[0])/2.0, 50*(prev_pt[1]-pt[1])/(prev_pt[0]-pt[0])+500) ) # Numerical approximation. Note: Weird scaling
			prev_pt = pt

		return deriv

	def integrate(self):
		"""
		Method that creates a list of tuples which is the integral of the current Line object.
		"""
		integral = []
		prev_pt = self.points[0]
		tr = 0.0    # Initial trapezoidal area
		C = 0   # Initial integration constant
		for pt in self.points[1:]:
			tr += trap((prev_pt[0]-500, prev_pt[1]-500), (pt[0]-500, pt[1]-500))    # Numerical approximation of integral
			x = (pt[0]+prev_pt[0])/2    # New x value

			if x < 500:             # Get the integration constant (integral from the first point to 0)
				C = tr

			int_pt = (x, tr)

			integral.append(int_pt)
			prev_pt = pt

		integral = [(pt[0], 500+(pt[1]-C)/100) for pt in integral] # WEIRD SCALING 
		return integral



if __name__ == '__main__':
	import matplotlib.pyplot as plt

	# Hardcoded points
	pts = [(20, 438), (43, 395), (90, 317), (160, 263), (213, 261), (291, 285), (379, 282), (468, 228), (544, 142), (598, 55), (609, 39)]
	# pts = [(79, 330), (81, 317), (88, 266), (108, 221), (170, 165), (246, 127), (333, 133), (375, 196), (366, 260), (316, 281), (275, 258), (260, 218), (304, 145), (365, 113), (478, 129), (556, 172), (584, 183)]
	# pts = [(1,1), (2,4), (3,9), (4,16), (5,25)]
	
	# pts = [(29, 204), (46, 204), (72, 201), (104, 200), (136, 209), (179, 233), (228, 278), (279, 304), (339, 302), (381, 274), (424, 240), (460, 227), (511, 227), (535, 224), (557, 224), (576, 224), (577, 224)]

	# pts = [(pt[0]-200, pt[1]-200) for pt in pts]

	pts = [(x, x**3/10-x+0.2) for x in list(np.linspace(0,1,10))]

	print pts

	c = Curve(pts)
	c.draw_to_plot()

	print 'done?'

