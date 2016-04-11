# from scipy.interpolate import interp1d
#import scipy
from scipy import interpolate
import numpy as np

class Curve(object):
	"""

	"""

	def __init__(self, points):
		self.line = Line(points)
		self.derivative = Line(self.line.derive(), smooth_bool=True)
		print self.derivative.points
		self.integral = Line(self.line.integrate(), smooth_bool=True)

	def move_point(self, handle, distance, line='line'):
		if line == 'line':
			self.line.move_point(handle, distance)

			self.derivative = Line(self.line.derive(), smooth_bool=True)
			self.integral = Line(self.line.integrate(), smooth_bool=True)

		elif line == 'derivative':
			self.derivative.move_point(handle, distance)

			self.line = Line(self.derivative.integrate(), smooth_bool=True)
			self.integral = Line(self.line.integrate(), smooth_bool=True)

		elif line == 'integral':
			self.integral.move_point(handle, distance)

			self.line = Line(self.integral.derive(), smooth_bool=True)
			self.derivative = Line(self.line.derive(), smooth_bool=True)

	def draw_to_plot(self, variables=['line', 'derivative', 'integral']):

		if any(var == 'line' for var in variables):
			print 'Plotting line'
			# print self.line.points
			xy_s = zip(*self.line.points)
			# print xy_s[1]
			plt.plot(xy_s[0], xy_s[1], 'r-')

		if any(var == 'derivative' for var in variables):
			print 'Plotting derivative'
			pts = [(pt[0], pt[1]) for pt in self.derivative.points]
			xy_d = zip(*pts)
			print xy_d[1]
			plt.plot(xy_d[0], xy_d[1], 'g-')

		if any(var == 'integral' for var in variables):
			print 'Plotting integral'
			xy_i = zip(*self.integral.points)
			# print xy_i[1]
			# print xy_i[1][10]
			plt.plot(xy_i[0], xy_i[1], 'b-')

		plt.show()

class Line(object):
	"""

	"""

	def __init__(self, points, pull_pts_num=7, smooth_bool=False):		
		print "Making Line"
		if smooth_bool:		# If the points are smooth, don't bother smoothening the curve
			self.points = points
			print len(points)
			self.pull_points = (0,0)#points[::len(points)/pull_pts_num]
		else:
			self.points, self.pull_points = self.smoothen(points, pull_pts_num=pull_pts_num)

	def __index__(self, idx):
		return self.points[idx]

	def deep_copy(self):
		return Line(self.points[:])

	def smoothen(self, points, pull_pts_num=3):
		unzip = zip(*points)	# unzip the (x,y) tuples into a list of x and a list of y
		x = unzip[0]
		y = unzip[1]

		interpol = interpolate.interp1d(x,y, kind='cubic')	# Magic interpolation

		# num_points = (x[-1] - x[0])
		num_points = 100

		xnew = np.linspace(x[0]+1, x[-1]-1, num_points)	# Smooth Line
		ynew = interpol(xnew)

		xpull = np.linspace(x[0]+1, x[-1]-1, pull_pts_num)	# Pulling Points
		ypull = interpol(xpull)

		return (zip(xnew, ynew), zip(xpull, ypull))			# zip the list of x and list of y into (x,y) tuples

	def move_point(self, index, distance, kind='relative'): # currently doesn't change the local Line
		pts = self.points
		distance = float(distance)

		if index >= len(pts):
			print 'Index out of Range'
			return None

		# pts[index] = (pts[index][0], pts[index][1] + distance)

		if kind == 'absolute':
			factor = 1.5
			# Absolute change in distance
			for i, pt in enumerate(pts[:index]):
				pts[i] = (pts[i][0], pts[i][1] + distance / (index-i+1)**2)
				print 'moved', distance / (index-i+1)

			for i, pt, in enumerate(pts[index:]):
				pts[i+index] = (pts[i+index][0], pts[i+index][1] + distance / (i+1)**2)
				print 'moved', distance / (i+1)

			# # Absolute change in distance
			# for i, pt in enumerate(pts[:index]):
			# 	pts[i] = (pts[i][0], pts[i][1] + distance * i / index)
			# 	print 'moved', distance / (index-i+1)

			# for i, pt, in enumerate(pts[index:]):
			# 	pts[i+index] = (pts[i+index][0], pts[i+index][1] + distance * (index-i) / index)
			# 	print 'moved', distance / (i+1)

		elif kind == 'relative':
			rel_d = distance / pts[index][1] 
			for i, pt in enumerate(pts[:index]):
				pts[i] = (pts[i][0], pts[i][1] * (1 + (rel_d / (index-i+1))))
				print 'moved', 1 + rel_d / (index-i+1)

			for i, pt, in enumerate(pts[index:]):
				pts[i+index] = (pts[i+index][0], pts[i+index][1] * (1 + (rel_d / (i+1))))
				print 'moved', 1 + rel_d / (i+1)
		else:
			print 'Invalid Version'
			return None


		self.update()
		return pts

	
	def derive(self):
		# print list(np.gradient(self.points))
		# print 'in derive()'

		deriv = []
		prev_pt = self.points[0]

		for pt in self.points[1:]:
			deriv.append( ((pt[0]+prev_pt[0])/2.0, (prev_pt[1]-pt[1])/(prev_pt[0]-pt[0])) )
			prev_pt = pt

		return deriv

		# grad = np.gradient(self.points)
		# ret = []
		# for pt in grad:
		# 	print pt[0], pt[1]
		# 	ret.append((pt[0], pt[1]))
		# return ret

	def integrate(self):
		integral = []
		prev_pt = self.points[0]

		tr = 0.0

		for pt in self.points[1:]:
			# integral.append(((pt[0]+prev_pt[0])/2, np.trapz([prev_pt[1], pt[1]], [prev_pt[0], pt[0]])))
			tr += trap(prev_pt, pt)
			int_pt = ((pt[0]+prev_pt[0])/2, tr)
			# print 'point:         ', prev_pt
			# print 'integral point:', int_pt
			integral.append(int_pt)
			prev_pt = pt

		return integral

def trap(a, b):
	"""
	Take points a, b which are (x,y) tuples, and find the trapezoidal area.
	"""
	dx = b[0]-a[0]
	return (a[1]+b[1])*dx/2.0



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




