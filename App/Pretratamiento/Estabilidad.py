import numpy as np

class Est():
	"""
		Evalúa la estabilidad en el centro del cubo,
		si hay réplicas...
	"""
	def __init__(self, datos):
		self.resultados = {}
		data000 = []
		for i in range(len(datos['Y'])):
			centro = True
			for key in datos:
				if key != 'Y' and datos[key][i] != 0:
					centro = False
			if centro:
				data000.append(datos['Y'][i])

		if len(data000) > 1:
			self.resultados['Promedio'] = np.mean(data000)
			self.resultados['Desvest'] = np.std(data000)
			self.resultados['CV [%]'] = \
				100*np.std(data000)/np.mean(data000)
			self.resultados['Varianza'] = np.var(data000, ddof=1)
			if self.resultados['CV [%]'] > 10:
				print("ADVERTENCIA: El coeficiente de variación (CV) está por encima del 10%")
		else:
			print('NO hay réplicas en el centro del cubo experimental')

		self.Filtrado(datos)

	def Filtrado(self, datos):
		"""
			Filtración de datos para planteamiento y validación. 

			Validación		Los datos NO presentes en la superficie del
							cubo.

			Planteamiento 	Datos presentes en la superficie del cubo.	
		"""
		self.Plant = {}
		self.Val = {}
		Primera = {}
		for key in datos:
			self.Plant[key] = []
			self.Val[key] = []
			Primera[key] = True
		for i in range(len(datos['Y'])):
			plant = True
			for key in datos:
				if key != 'Y':
					if datos[key][i] != -1 and datos[key][i] != 0 and \
							datos[key][i] != 1:
						if not Primera[key]:
							plant = False
						else:
							Primera[key] = False
			for key in datos:
				if plant:
					self.Plant[key].append(datos[key][i])
				else:
					self.Val[key].append(datos[key][i])

	def __call__(self):
		return self.resultados
