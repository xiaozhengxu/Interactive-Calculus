# from scipy.interpolate import interp1d
#import scipy
from scipy import interpolate
import numpy as np

class Curve(object):
	"""

	"""

	def __init__(self, points):
		self.points = points
		self.update()

	def deep_copy(self):
		return Curve(self.points[:])

	def update(self):
		self.smooth = self.smoothen()
		self.derivative = self.derive()
		self.integral = self.integrate()


	def derive(self):
		return list(np.gradient(self.smooth))

	def integrate(self):
		integral = []
		prev_pt = self.points[0]

		for pt in self.points[1:]:
			integral.append(np.trapz([prev_pt[1], pt[1]], [prev_pt[0], pt[0]]))

		return integral

	def smoothen(self):
		# x = [tup[0] for tup in self.points]
		# y = [tup[1] for tup in self.points]
		#sorted_pts = sorted(self.points, key=lambda point: point[0])
		# sorted_pts = sorted(self.points)

		#unzip = zip(*sorted_pts)
		unzip = zip(*self.points)
		x = unzip[0]
		y = unzip[1]

		# print 'x=', x, type(x)
		# print 'y=', y, type(y)

		interpol = interpolate.interp1d(x,y, kind='cubic')

		xnew = np.linspace(x[0]+1, x[-1]-1, (x[-1] - x[0]))
		ynew = interpol(xnew)
		# ynew = np.interp(xnew, x, y)

		return zip(xnew, ynew)

	def move_point(self, index, distance, kind='absolute'): # currently doesn't change the local curve
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

	def draw_to_plot(self, variables=['smooth', 'derivative', 'integral']):

		if any(variables) == 'smooth':
			xy_s = zip(*self.smooth)
			plt.plot(xy_s[0], xy_s[1], 'r-')

		if any(variables) == 'derivative':
			xy_d = zip(*self.derivative)
			plt.plot(xy_d[0], xy_d[1], 'g-')

		if any(variables) == 'integral':
			xy_i = zip(*self.integral)
			plt.plot(xy_i[0], xy_i[1], 'b-')



if __name__ == '__main__':
	import matplotlib.pyplot as plt

	# Hardcoded points
	pts = [(20, 438), (43, 395), (90, 317), (160, 263), (213, 261), (291, 285), (379, 282), (468, 228), (544, 142), (598, 55), (609, 39)]
	# pts = [(79, 330), (81, 317), (88, 266), (108, 221), (170, 165), (246, 127), (333, 133), (375, 196), (366, 260), (316, 281), (275, 258), (260, 218), (304, 145), (365, 113), (478, 129), (556, 172), (584, 183)]
	# pts = [(1,1), (2,4), (3,9), (4,16), (5,25)]


	pts = [(29, 204), (46, 204), (72, 201), (104, 200), (136, 209), (179, 233), (228, 278), (279, 304), (339, 302), (381, 274), (424, 240), (460, 227), (511, 227), (535, 224), (557, 224), (576, 224), (577, 224)]

	xy = zip(*pts)
	print xy

	# Make a curve object
	c = Curve(pts)
	c2 = c.deep_copy()
	c2.move_point(8,-30, kind='absolute')

	m_xy = zip(*c2.points)

	xynew = zip(*c.smooth)
	xymoved = zip(*c2.smooth)

	# c.draw_to_plot(plt)

	# plt.show()
	plt.plot(xy[0], xy[1], 'o' , xynew[0], xynew[1], '-',m_xy[0], m_xy[1], 'o',  xymoved[0], xymoved[1], '+')
	# plt.plot(xy[0], xy[1], 'o' ,m_xy[0], m_xy[1], '+')
	plt.show()



