import matplotlib.pyplot as plt

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

	def __init__(self, Modelo):
		pass