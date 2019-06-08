import numpy as np
import itertools as it
import matplotlib.pyplot as plt
from scipy.stats import norm

class NormalDist():
	"""
		Datos para la gráfica de distribución normal
	"""
	def __init__(self, data):
		self.NormG = {}
		comb = self.Combinaciones(data)
		self.CombMatrix(comb, data)
		self.Orden()
		self.FractionZ()

	def FractionZ(self):
		nT = 0
		for key in self.NormG:
			nT += 1
		for key in self.NormG:
			self.NormG[key]['Fracción'] = (self.NormG[key]['Orden']-0.5)/nT
			self.NormG[key]['Z'] = norm.ppf(self.NormG[key]['Fracción'])
		self.NormG['N_Datos'] = len(self.NormG[key]['Vector'])



	def Orden(self):
		datos = [[], []]
		for var in self.NormG:
			datos[0].append(self.NormG[var]['X'])
		datos[1] = np.searchsorted(np.sort(datos[0]), datos[0], side='left')

		for var in self.NormG:
			for i in range(len(datos[0])):
				if datos[0][i] == self.NormG[var]['X']:
					self.NormG[var]['Orden'] = datos[1][i]

	def CombMatrix(self, combinaciones, data):
		for key in data:
			if key != 'Y':
				self.NormG[key] = {}
				self.NormG[key]['Vector'] = data[key]

		for var in self.NormG:
			for var2 in data:
				#¿Es una combinación?
				if var != var2:
					self.NormG[var]['Vector'] = []
					suma = 0
					for i in range(len(data['Y'])):
						num_ant = 1
						for letra in var:
							num = num_ant*data[letra][i]
							num_ant = num
						suma += num*data['Y'][i]
						self.NormG[var]['Vector'].append(num)
					self.NormG[var]['X'] = suma/8
	
	def Combinaciones(self, data):
		#TODAS las posibles combinaciones
		Encabezados = []
		comb = []
		for key in data:
			if key != 'Y':
				Encabezados.append(key)

		for i in range(len(Encabezados)):
			if i < len(Encabezados):
				comb.append(list(it.combinations(\
					Encabezados, i+1)))

		#Inicialización variables del diccionario
		combs = []
		for combinaciones in comb:
			for combinacion in combinaciones:
				c = ''
				for letra in combinacion:
					c += letra[0]
				combs.append(c)
				self.NormG[c] = {}
		return combs

class NormalGraph(NormalDist):
	"""
		Gráfica de distribución normal
	"""
	def __init__(self, data):
		self.Ejes = {
			'x':[],
			'Z':[],
			'Nombres': []
		}
		super().__init__(data)
		self.fig = plt.figure()
		self.ax = self.fig.add_subplot(111)

		self.Axes()

		self.ax.scatter(
				self.Ejes['x'],
				self.Ejes['Z']
			)

		self.ax.set_xlabel('Data')
		self.ax.set_ylabel('Z')
		self.ax.set_title('Gráfica de Distribución Normal')
		self.ax.grid()

		#print(np.sort(self.Ejes['x']), np.sort(self.Ejes['Z']))

	def Axes(self):
		for var in self.NormG:
			if var != 'N_Datos':
				self.Ejes['x'].append(self.NormG[var]['X'])
				self.Ejes['Z'].append(self.NormG[var]['Z'])
				self.Ejes['Nombres'].append(var)
		

	def __call__(self):
		return self.NormG

if __name__ == '__main__':
	data = {
		'A': [1,0,-1,1],
		'B': [1,1,0,1],
		'C': [1,1,0,-1],
		'D': [0,0,0,0],
		'Y': [1,1.5,2,2.5]
	}
	NormalGraph(data)