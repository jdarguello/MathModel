import numpy as np
import itertools as it
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib.ticker import PercentFormatter

class NormalDist():
	"""
		Datos para la gráfica de distribución normal y 
		diragrama de pareto
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

class Pareto(NormalDist):
	"""
		Diagrama de pareto:	Consiste de una gráfica de barras y una 
							línea de tendencia porcentual.

		Gráfica de barras:	Eje y -> sumaproducto **2 / 16
							Eje x -> nombre de combinación

		Línea de tendencia:	Eje y -> porcentaje acumulado
							Eje x -> nombre de combinación

	"""
	def __init__(self, data, porcentaje, grid=False, size = False):
		super().__init__(data)
		resul_grafico = self.ProcesamientoDatos(data['Y'], porcentaje)
		self.Diagrama(resul_grafico, grid, size)

	def Diagrama(self, res, grid, size):
		fig, ax = plt.subplots()
		if size:
			fig.set_size_inches(size[0], size[1])
		x = [comb[0] for comb in res['Bar']['Ordenado']]
		y = [comb[1] for comb in res['Bar']['Ordenado']]
		y2 = res['Per']['PorAc']
		ax.bar(x, y, color='C0')
		ax2 = ax.twinx()
		ax2.plot(x, y2, color='C1', marker='D', ms=7)
		ax2.yaxis.set_major_formatter(PercentFormatter())

		ax.tick_params(axis='y', colors='C0')
		ax2.tick_params(axis='y', colors='C1')

		if grid:
			ax.grid()

		ax.set_title('Diagrama de pareto')
		ax.set_ylim([0, res['Bar']['Total']])
		ax2.set_ylim([0, 100])

		plt.show()


	def ProcesamientoDatos(self, Y, porcentaje):
		#Listas ordenadas de mayor a menor
		res = {
			'Bar': {
				'Inicial':{
					'SumP': [],
					'Nombres': []
				},
				'Ordenado':[],
				'Total': 0
			},
			'Per': {
				'PorAc': [],
				'Nombres':[]
			}
		}

		#Diagrama de barras
		for key in self.NormG:
			try:
				res['Bar']['Inicial']['SumP'].append((np.dot(
						np.array(self.NormG[key]['Vector']),
						np.array(Y)
					)**2)/16)
				res['Bar']['Inicial']['Nombres'].append(key)
			except:
				pass

		dtype = [('Combination', 'U10'), ('Value', 'f4')]
		lista = []
		for i in range(len(res['Bar']['Inicial']['SumP'])):
			lista.append((
						res['Bar']['Inicial']['Nombres'][i],
						res['Bar']['Inicial']['SumP'][i]
						))
			res['Bar']['Total'] += res['Bar']['Inicial']['SumP'][i]
		res['Bar']['Ordenado'] = np.sort(np.array(
				lista, dtype = dtype
			), order='Value')[::-1]

		#Línea de tendencia
		self.ef = []	#Variables de mayor efecto
		por_ant = 0
		for i in range(len(res['Bar']['Inicial']['SumP'])):
			por = (res['Bar']['Ordenado'][i][1]/res['Bar']['Total'])*100 + por_ant
			res['Per']['Nombres'].append(res['Bar']['Ordenado'][i][0])
			if por < porcentaje:
				self.ef.append(res['Bar']['Ordenado'][i][0])
			res['Per']['PorAc'].append(por.round(3))
			por_ant = por
		self.ef = tuple(self.ef)
		return res

class NormalGraph(NormalDist):
	"""
		Gráfica de distribución normal
	"""
	def __init__(self, data, size=False):
		self.Ejes = {
			'x':[],
			'Z':[],
			'Nombres': []
		}
		super().__init__(data)
		self.fig = plt.figure()
		self.ax = self.fig.add_subplot(111)
		if size:
			self.fig.set_size_inches(size[0], size[1])

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
		'D': [1,1,1,1],
		'Y': [5,3.5,2,2.5]
	}
	Dist = NormalDist(data)
	#print(Dist.NormG)

	pareto = Pareto(data, True)