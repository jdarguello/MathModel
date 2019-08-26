import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patches as pt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

class ExpCube():
	"""
		Developement and printing of the experimental cube 
		(2D and 3D only)
	"""
	points3D = np.array([[-1, -1, -1],
                  [1, -1, -1 ],
                  [1, 1, -1],
                  [-1, 1, -1],
                  [-1, -1, 1],
                  [1, -1, 1 ],
                  [1, 1, 1],
                  [-1, 1, 1]])
	points2D = np.array([[-1,-1],
				[1,-1],
				[1,1],
				[-1,1]])
	def __init__(self, data, lang = 'Spanish'):
		num = 0
		datos = []
		for key in data:
			if key != 'Y':
				datos.append(data[key])
				num += 1
		#Diagram
		if num == 1:
			print('1D...')
		elif num == 2:
			self.D2(datos, lang, data)
		elif num == 3:
			self.D3(datos, lang, data)
		else:
			if lang == 'English':
				print('Bigger than 3D')
			else:
				print('Mayor a 3D')
	def D2(self, data, lang, original):
		fig = plt.figure()
		ax = fig.add_subplot(111)

		col = pt.Polygon(self.points2D, linewidth=1, edgecolor='b', alpha=.25)
		ax.add_patch(col)
		ax.scatter(data[0], data[1])
		primera = [True, True]
		for label in original:
			if label != 'Y':
				if primera[0]:
					ax.set_xlabel(label)
					primera[0] = False
				elif primera[1]:
					ax.set_ylabel(label)
					primera[1] = False
		if lang == 'Spanish':
			ax.set_title('Cubo Experimental')
		else:
			ax.set_title('Experimental Cube')
		plt.show()

	def D3(self, data, lang, original):
		fig = plt.figure()
		ax = fig.gca(projection='3d')
		
		#X, Y = np.meshgrid([-1, 1], [-1, 1])
		ax.scatter3D(self.points3D[:,0], self.points3D[:, 1],\
			 self.points3D[:,2])
		verts = [[self.points3D[0],self.points3D[1],self.points3D[2],self.points3D[3]],
		 [self.points3D[4],self.points3D[5],self.points3D[6],self.points3D[7]], 
		 [self.points3D[0],self.points3D[1],self.points3D[5], self.points3D[4]], 
		 [self.points3D[2],self.points3D[3],self.points3D[7],self.points3D[6]], 
		 [self.points3D[1],self.points3D[2],self.points3D[6],self.points3D[5]],
		 [self.points3D[4],self.points3D[7],self.points3D[3],self.points3D[0]]]

		# plot sides
		col = Poly3DCollection(verts, 
		 facecolors='cyan', linewidths=1, edgecolors='b', alpha=.25)
		face_color = [0.5, 0.5, 1]
		col.set_facecolor(face_color)
		ax.add_collection3d(col)
		ax.scatter3D(data[0], data[1], data[2])
		primera = [True, True, True]
		for label in original:
			if label != 'Y':
				if primera[0]:
					ax.set_xlabel(label)
					primera[0] = False
				elif primera[1]:
					ax.set_ylabel(label)
					primera[1] = False
				elif primera[2]:
					ax.set_zlabel(label)
					primera[2] = False
		if lang == 'English':
			ax.set_title('Experimental Cube')
		else:
			ax.set_title('Cubo Experimental')
		plt.show()	
		
if __name__ == '__main__':
	datos = {
		'A': [1,0,2,1.5],
		'B': [0,0,1,2],
		'Y': [0,0,0,0]
	}
	ExpCube(datos)