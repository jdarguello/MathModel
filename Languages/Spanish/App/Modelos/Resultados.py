import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Ys():
	"""
		Gráfica de Y vs Y calculado
	"""
	def __init__(self, Modelo, Y):
		Ejes = self.Data(Modelo, Y)
		self.Esquema(x = Ejes['x'], y = Ejes['y'], x_t = 'Y',\
			 y_t = 'Ycal', title='Y vs Ycal')

	def Data(self, Modelo, Y):
		#Inicialización
		Ejes = {
			'x': Y,
			'y': Modelo['Ycal']
		}
		return Ejes

	def Esquema(self, **args):
		fig = plt.figure()
		ax = fig.add_subplot(111)

		ax.scatter(
				args['x'],
				args['y']
			)

		ax.set_xlabel(args['x_t'])
		ax.set_ylabel(args['y_t'])
		ax.set_title(args['title'])
		ax.grid()

class Residuo(Ys):
	"""
		Grafica el residuo del modelo planteado
	"""
	def __init__(self, Modelo, Y):
		Ejes = self.Axes(Modelo, Y)
		self.Esquema(x = Ejes['x'], y = Ejes['y'], x_t = 'Y',\
			 y_t = 'Yi-Ycal', title='Residuo')

	def Axes(self, Modelo, Y):
		Ejes = {
			'x': Y,
			'y': Modelo['Yi-Ycal']
		}
		return Ejes

class SuperficieRespuesta():
	"""
		Genera la superficie de respuesta en 3D
	"""

	def __init__(self, Modelo, limits, puntos = 100):
		var_T = self.GraphDim(Modelo)

		#Selección del camino
		if len(var_T) == 3:
			Ejes = self.Axes4D(Modelo, limits, var_T, puntos)

		#Desarrollo del esquema
		self.Esquema(Ejes, var_T)

	def Esquema(self, Ejes, var_T):
		#Color
		color_dimension = Ejes[4]
		minn, maxx = color_dimension.min(), color_dimension.max()
		norm = matplotlib.colors.Normalize(minn, maxx)
		m = plt.cm.ScalarMappable(norm=norm, cmap='jet')
		m.set_array([])
		fcolors = m.to_rgba(color_dimension)


		#Gráfica
		fig = plt.figure()
		ax = fig.gca(projection='3d')
		ax.plot_surface(
			Ejes[0],
			 Ejes[1],
			  Ejes[3])
		ax.set_xlabel(var_T[0])
		ax.set_ylabel(var_T[1])
		ax.set_zlabel('Y')
		plt.show()

	def Axes4D(self, Modelo, limits, var_T, puntos):
		Ejes = []
		for i in range(len(var_T)):
			Ejes.append(np.arange(
				limits[var_T[i]]['-1'], 
				limits[var_T[i]]['1'],
				(limits[var_T[i]]['1']-limits[var_T[i]]['-1'])/puntos))
		
		X, Y = np.meshgrid(Ejes[0], Ejes[1])
		C = np.zeros((len(X),len(X)))
		for i in range(len(X)):
			C[i] = np.arange(
				limits['C']['-1'], 
				limits['C']['1'],
				(limits['C']['1']-limits['C']['-1'])/puntos)
		vec = [X, Y, C]
		dic = {}
		for i in range(len(var_T)):
			dic[var_T[i]] = np.ravel(vec[i])

		zs = np.array(self.EqConversion(Ecuacion = Modelo['Ecuación'], \
			Variables = dic))
		Z = zs.reshape(X.shape)

		return X,Y,C,Z, Ejes[2]

	def EqConversion(self, **Modelo):
		#Evalúa la respuesta de los puntos del modelo matemático
		text = ''
		for i in range(len(Modelo['Ecuacion'])):
			if i != 0:
				text += '+'
			for j in range(len(Modelo['Ecuacion'][i])):
				if j < len(Modelo['Ecuacion'][i]) -1:
					op = '*'
				else:
					op = ''
				try:
					int(Modelo['Ecuacion'][i][j])
					text += '**' + Modelo['Ecuacion'][i][j] + ')' + op
				except:
					text += '(' + Modelo['Ecuacion'][i][j]
		return eval(text, Modelo['Variables'])

	def GraphDim(self, Modelo):
		#Determinar la dimensión a graficar
		var = []
		for key in Modelo['Variables']:
			for key2 in Modelo['Variables'][key]['Exponentes']:
				Existe = False
				for i in range(len(var)):
					if var[i] == key2:
						Existe = True
				if not Existe:
					var.append(key2)
		return var

if __name__ == '__main__':
	Modelo = {
		'Ecuación': ('A1',
  'A2',
  'A1B1',
  'A2B1',
  'C1',
  'C2',
  'B1',
  'B2',
  'A1C2',
  'A2C2'),
 'Variables': {'A1': {'Exponentes': {'A': 1},
   'Vector': np.array([-1.,  1., -1.,  1., -1.,  1., -1.,  1.,  0.,  0.,  2.,  1., -1.,
           0.,  0.,  0.,  0.,  0.,  1., -1.,  0.,  0.])},
  'A2': {'Exponentes': {'A': 2},
   'Vector': np.array([1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 4., 1., 1., 0., 0., 0., 0.,
          0., 1., 1., 0., 0.])},
  'A1B1': {'Exponentes': {'A': 1, 'B': 1},
   'Vector': np.array([ 1., -1., -1.,  1.,  1., -1., -1.,  1.,  0.,  0.,  0.,  1.,  1.,
           0.,  0.,  0.,  0.,  0.,  0., -0.,  0., -0.])},
  'A2B1': {'Exponentes': {'A': 2, 'B': 1},
   'Vector': np.array([-1., -1.,  1.,  1., -1., -1.,  1.,  1.,  0.,  0.,  0.,  1., -1.,
           0.,  0.,  0.,  0.,  0.,  0.,  0.,  0., -0.])},
  'C1': {'Exponentes': {'C': 1},
   'Vector': np.array([-1., -1., -1., -1.,  1.,  1.,  1.,  1.,  2.,  0.,  0.,  0.,  0.,
           0.,  0.,  0.,  0.,  0.,  1., -1.,  1., -1.])},
  'C2': {'Exponentes': {'C': 2},
   'Vector': np.array([1., 1., 1., 1., 1., 1., 1., 1., 4., 0., 0., 0., 0., 0., 0., 0., 0.,
          0., 1., 1., 1., 1.])},
  'B1': {'Exponentes': {'B': 1},
   'Vector': np.array([-1., -1.,  1.,  1., -1., -1.,  1.,  1.,  0.,  2.,  0.,  1., -1.,
           0.,  0.,  0.,  0.,  0.,  0.,  0.,  1., -1.])},
  'B2': {'Exponentes': {'B': 2},
   'Vector': np.array([1., 1., 1., 1., 1., 1., 1., 1., 0., 4., 0., 1., 1., 0., 0., 0., 0.,
          0., 0., 0., 1., 1.])},
  'A1C2': {'Exponentes': {'A': 1, 'C': 2},
   'Vector': np.array([-1.,  1., -1.,  1., -1.,  1., -1.,  1.,  0.,  0.,  0.,  0., -0.,
           0.,  0.,  0.,  0.,  0.,  1., -1.,  0.,  0.])},
  'A2C2': {'Exponentes': {'A': 2, 'C': 2},
   'Vector': np.array([1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
          0., 1., 1., 0., 0.])}},
 'Matriz exp': np.array([[ 1., -1.,  1.,  1., -1., -1.,  1., -1.,  1., -1.,  1.],
        [ 1.,  1.,  1., -1., -1., -1.,  1., -1.,  1.,  1.,  1.],
        [ 1., -1.,  1., -1.,  1., -1.,  1.,  1.,  1., -1.,  1.],
        [ 1.,  1.,  1.,  1.,  1., -1.,  1.,  1.,  1.,  1.,  1.],
        [ 1., -1.,  1.,  1., -1.,  1.,  1., -1.,  1., -1.,  1.],
        [ 1.,  1.,  1., -1., -1.,  1.,  1., -1.,  1.,  1.,  1.],
        [ 1., -1.,  1., -1.,  1.,  1.,  1.,  1.,  1., -1.,  1.],
        [ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.],
        [ 1.,  0.,  0.,  0.,  0.,  2.,  4.,  0.,  0.,  0.,  0.],
        [ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  2.,  4.,  0.,  0.],
        [ 1.,  2.,  4.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
        [ 1.,  1.,  1.,  1.,  1.,  0.,  0.,  1.,  1.,  0.,  0.],
        [ 1., -1.,  1.,  1., -1.,  0.,  0., -1.,  1., -0.,  0.],
        [ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
        [ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
        [ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
        [ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
        [ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
        [ 1.,  1.,  1.,  0.,  0.,  1.,  1.,  0.,  0.,  1.,  1.],
        [ 1., -1.,  1., -0.,  0., -1.,  1.,  0.,  0., -1.,  1.],
        [ 1.,  0.,  0.,  0.,  0.,  1.,  1.,  1.,  1.,  0.,  0.],
        [ 1.,  0.,  0., -0., -0., -1.,  1., -1.,  1.,  0.,  0.]]),
 'Bs': np.array([ 2.77056677,  4.78040748,  0.60167307,  1.97778701, -1.27638381,
         0.93692583,  0.21525236,  1.17040232, -0.54467489, -4.69529264,
         1.85034771]),
 'Ycal': np.array([ 5.95489286,  2.16954851,  1.78735586,  5.91315954,  7.82874452,
         4.04340017,  3.66120751,  7.7870112 ,  5.50542788,  2.93267185,
        14.73807402,  9.47977794,  0.13092598,  2.77056677,  2.77056677,
         2.77056677,  2.77056677,  2.77056677,  6.45988057,  4.41579925,
         4.54847239,  0.3338161 ]),
 'Yi-Ycal': np.array([ 0.11810714,  0.27745149, -0.22835586, -0.16815954, -0.02974452,
        -0.37640017,  0.20179249,  0.4139888 ,  0.27157212,  0.33432815,
         0.11492598, -0.34477794, -0.11492598,  0.39343323, -0.42956677,
         0.37943323,  0.01843323,  0.46343323, -0.14688057, -0.06179925,
        -0.87747239, -0.2088161 ]),
 'Yi-Yexpprom': np.array([ 1.45740909, -2.16859091, -3.05659091,  1.12940909,  3.18340909,
        -0.94859091, -0.75259091,  3.58540909,  1.16140909, -1.34859091,
        10.23740909,  4.51940909, -4.59959091, -1.45159091, -2.27459091,
        -1.46559091, -1.82659091, -1.38159091,  1.69740909, -0.26159091,
        -0.94459091, -4.49059091]),
 'R2': 0.9895966100923922,
 'R2aju': 0.9801389829036579
	}
	limits = {
	    'A':{
	        '-1':3,
	        '1':8
	    },
	    'B':{
	        '-1':30,
	        '1':60
	    },
	    'C':{
	        '-1':8,
	        '1':20
	    }
	}
	SuperficieRespuesta(Modelo, limits)