import numpy as np
import matplotlib.pyplot as plt
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
	def __init__(self, data):
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
			self.D2(datos)
		elif num == 3:
			self.D3(datos)
		else:
			print('Bigger than 3D')
	def D2(self, data):
		pass

	def D3(self, data):
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

		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')
		plt.show()	
		
if __name__ == '__main__':
	datos = {
		'A': [1,0,2,1.5],
		'B': [0,0,1,2],
		'C': [1,1,0,1],
		'Y': [0,0,0,0]
	}
	ExpCube(datos)