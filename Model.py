import curve
import view


class Model(object):
	"""
	The main model class to keep track of everythg display related
	"""

	def __init__(self):
		self.grid_status = True
		self.legend_status = True
		


	def grid_update(self):
		"""
		To keep track of the state of the grid
		"""
		if self.grid_status == True:
			self.grid_status = False
		elif self.grid_status == False:
			self.grid_status = True
		

		return self.grid_status




	def update(self):
		"""
		To update the model accoring to user input
		"""
		pass

