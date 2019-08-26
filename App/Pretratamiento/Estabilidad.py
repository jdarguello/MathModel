import numpy as np

class Est():
	"""
		Evalúa la estabilidad en el centro del cubo,
		si hay réplicas...
	"""
	def __init__(self, datos, lang = 'Spanish'):
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
				if lang == "English":
					print('WARNING: the variation coeficient is above the 10%')
				else:
					print("ADVERTENCIA: El coeficiente de variación (CV) está por encima del 10%")
		else:
			if lang == 'English':
				print('There is NOT enough data in the center of the experimental cube')
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
		#Inicialización de variables
		num_var = 0
		for dat in datos:
			self.Plant[dat] = []
			self.Val[dat] = []
			num_var += 1
		num_var -= 1
		#Clasificación de la información
		for i in range(len(datos[dat])):
			#Revision
			plant = True
			for dat in datos:
				if dat != 'Y':
					if datos[dat][i] != 0 and datos[dat][i] != 1 \
						and datos[dat][i] != -1:
						plant = False
			#Save
			for dat in datos:
				if plant:
					self.Plant[dat].append(datos[dat][i])
				else:
					self.Val[dat].append(datos[dat][i])
		#New line of var
		

	def __call__(self):
		return self.resultados

if __name__ == '__main__':
	data = {
		'A': [0,0,0,1,1.5,1,0, -1],
		'B': [0,0,0,2,1,1,0, -1],
		'C': [0,0,0,0,1,0.5,1,-1],
		'Y': [1.2, 1.5, 1.35, 0.9, 1.5, 2.2, 2, 2.5]
	}
	datos = Est(data)
	print(datos.Val)