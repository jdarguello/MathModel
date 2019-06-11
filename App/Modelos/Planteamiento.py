import numpy as np
import itertools as it
import math

from App.DataBase.db import *

class Planteamiento():
	"""
		Plantear la mayoría de los modelos matemáticos posibles.
	"""

	def __init__(self, datos, NormDist, nombre):
		self.Mejores = {}
		#Creación base de datos
		nombre = 'App/DataBase/' + nombre
		BD = DataBase(nombre)
		BD.Create()

		#Llenado de la base de datos
		self.Combinaciones(datos, NormDist, nombre)

		#self.Selection()

	def Selection(self):
		Rmax = 0
		for var in self.Planteamiento:
			if self.Planteamiento[var]['R2aj'] > Rmax:
				Rmax = self.Planteamiento[var]['R2aj']

		for var in self.Planteamiento:
			if self.Planteamiento[var]['R2aj'] == Rmax:
				self.Mejores = {
					'Ecuación': self.Planteamiento[var]['Ecuación'],
					'Matriz exp': self.Planteamiento[var]['Matriz exp'],
					'Bs': self.Planteamiento[var]['Bs'],
					'Ycal': self.Planteamiento[var]['Ycal'],
					'R2': self.Planteamiento[var]['R2'],
					'R2aj': self.Planteamiento[var]['R2aj']
				}
			

	def Calculos(self, Ecu, datos, NormDist, nombre, cont):
		try:
			dic = {}
			dic[cont] = {
				'Ecuación':Ecu,
				'Variables': {}
			}
			M = []
			onevec = []
			for i in range(NormDist['N_Datos']):
				onevec.append(1)
			M.append(onevec)
			for i in range(len(Ecu)):
				dic[cont]['Variables'][Ecu[i]] = \
					NormDist[Ecu[i]]['Vector']
				M.append(NormDist[Ecu[i]]['Vector'])
			dic[cont]['Matriz exp'] = np.transpose(np.array(M))
			dic[cont]['Bs'] = np.matmul(
				np.matmul(
					np.linalg.inv(np.matmul(
						np.transpose(dic[cont]['Matriz exp']),
						dic[cont]['Matriz exp']
						)),
					np.transpose(
						dic[cont]['Matriz exp'])), 
				np.transpose(datos['Y'])
				)
			dic[cont]['Ycal'] = np.matmul(
				dic[cont]['Matriz exp'],
				dic[cont]['Bs']
				)

			#Yi - Ycal, Yi - Yexpprom
			dic[cont]['Yi-Ycal'] = np.zeros(NormDist['N_Datos'])
			dic[cont]['Yi-Yexpprom'] = np.zeros(NormDist['N_Datos'])
			for i in range(NormDist['N_Datos']):
				dic[cont]['Yi-Ycal'][i] = \
					datos['Y'][i] - dic[cont]['Ycal'][i]
				dic[cont]['Yi-Yexpprom'][i] = \
					datos['Y'][i] - np.mean(datos['Y'])
			SSreg = np.sum(dic[cont]['Yi-Ycal']**2)
			SStot = np.sum(dic[cont]['Yi-Yexpprom']**2)
			dic[cont]['R2'] = (SStot-\
					SSreg)/SStot
			dic[cont]['R2aju'] = \
				(SStot/(NormDist['N_Datos']-1)-\
					SSreg/(NormDist['N_Datos']-\
						len(dic[cont]['Ecuación'])-\
						1))/(SStot/(NormDist['N_Datos']-1))

			self.Guardar(dic, nombre)
		except:
			pass

	def Guardar(self, dic, nombre):
		model = Modelo(nombre, dic)
		model.Create()

	def Combinaciones(self, datos, NormDist, nombre):
		Encabezados = []
		cant_var_ini = 0
		for var in datos:
			if var != "Y":
				cant_var_ini += 1
				Encabezados.append(var)

		combinaciones = []
		for i in range(len(Encabezados)):
			if i < len(Encabezados):
				combinaciones.append(list(it.combinations(\
					Encabezados, i+1)))

		Total_Var = 0
		for comb in combinaciones:
			for comb2 in comb:
				Total_Var += 1

		#Pretratamiento
		comb = combinaciones
		combs = []
		for combinaciones in comb:
			for combinacion in combinaciones:
				c = ''
				for letra in combinacion:
					c += letra[0]
				combs.append(c)

		for i in range(Total_Var):
			self.combinations(combs, i+1, datos, NormDist, nombre)

	def combinations(self, iterable, r, datos, NormDist, nombre):
		pool = tuple(iterable)
		n = len(pool)
		if r > n:
			return
		indices = list(range(r))
		cont = 1
		while True:
			Ec = list(pool[i] for i in indices)
			self.Calculos(Ec, datos, NormDist, nombre, cont)
			for i in reversed(range(r)):
				if indices[i] != i + n - r:
					break
			else:
				return
			indices[i]  += 1
			
			for j in range(i+1, r):
				indices[j] = indices[j-1] + 1
			cont += 1

	def __call__(self):
		return self.Mejores

if __name__ == '__main__':
	datos = {'A': [-1.0,
	  1.0,
	  -1.0,
	  1.0,
	  -1.0,
	  1.0,
	  -1.0,
	  1.0,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  2.0,
	  -2.0,
	  0.0,
	  0.0,
	  1.5,
	  -1.5,
	  0.0,
	  0.0,
	  1.0,
	  -1.0,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  1.0,
	  -1.0,
	  0.0,
	  0.0],
	 'B': [-1.0,
	  -1.0,
	  1.0,
	  1.0,
	  -1.0,
	  -1.0,
	  1.0,
	  1.0,
	  0.0,
	  0.0,
	  2.0,
	  -2.0,
	  0.0,
	  0.0,
	  1.5,
	  -1.5,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  1.0,
	  -1.0,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  1.0,
	  -1.0],
	 'C': [-1.0,
	  -1.0,
	  -1.0,
	  -1.0,
	  1.0,
	  1.0,
	  1.0,
	  1.0,
	  2.0,
	  -2.0,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  1.5,
	  -1.5,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  0.0,
	  1.0,
	  -1.0,
	  1.0,
	  -1.0],
	 'Y': [6.073,
	  2.447,
	  1.559,
	  5.745,
	  7.799,
	  3.667,
	  3.863,
	  8.201,
	  5.777,
	  0.832,
	  3.267,
	  2.705,
	  14.853,
	  9.35,
	  3.129,
	  2.973,
	  8.642,
	  6.511,
	  4.689,
	  1.418,
	  9.135,
	  0.016,
	  3.164,
	  2.341,
	  3.15,
	  2.789,
	  3.234,
	  6.313,
	  4.354,
	  3.671,
	  0.125]}

	NormDist = {'A': {'Vector': [-1.0,
		   1.0,
		   -1.0,
		   1.0,
		   -1.0,
		   1.0,
		   -1.0,
		   1.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   2.0,
		   -2.0,
		   0.0,
		   0.0,
		   1.5,
		   -1.5,
		   0.0,
		   0.0,
		   1.0,
		   -1.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   1.0,
		   -1.0,
		   0.0,
		   0.0],
		  'X': 3.2558124999999998,
		  'Orden': 4,
		  'Fracción': 0.5833333333333334,
		  'Z': 0.21042839424792484},
		 'B': {'Vector': [-1.0,
		   -1.0,
		   1.0,
		   1.0,
		   -1.0,
		   -1.0,
		   1.0,
		   1.0,
		   0.0,
		   0.0,
		   2.0,
		   -2.0,
		   0.0,
		   0.0,
		   1.5,
		   -1.5,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   1.0,
		   -1.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   1.0,
		   -1.0],
		  'X': 1.675625,
		  'Orden': 2,
		  'Fracción': 0.25,
		  'Z': -0.6744897501960817},
		 'C': {'Vector': [-1.0,
		   -1.0,
		   -1.0,
		   -1.0,
		   1.0,
		   1.0,
		   1.0,
		   1.0,
		   2.0,
		   -2.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   1.5,
		   -1.5,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   1.0,
		   -1.0,
		   1.0,
		   -1.0],
		  'X': 3.5009375,
		  'Orden': 5,
		  'Fracción': 0.75,
		  'Z': 0.6744897501960817},
		 'AB': {'Vector': [1.0,
		   -1.0,
		   -1.0,
		   1.0,
		   1.0,
		   -1.0,
		   -1.0,
		   1.0,
		   0.0,
		   0.0,
		   0.0,
		   -0.0,
		   0.0,
		   -0.0,
		   0.0,
		   -0.0,
		   0.0,
		   -0.0,
		   0.0,
		   0.0,
		   1.0,
		   1.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   -0.0,
		   0.0,
		   -0.0],
		  'X': 3.179125,
		  'Orden': 3,
		  'Fracción': 0.4166666666666667,
		  'Z': -0.2104283942479247},
		 'AC': {'Vector': [1.0,
		   -1.0,
		   1.0,
		   -1.0,
		   -1.0,
		   1.0,
		   -1.0,
		   1.0,
		   0.0,
		   -0.0,
		   0.0,
		   0.0,
		   0.0,
		   -0.0,
		   0.0,
		   0.0,
		   0.0,
		   -0.0,
		   0.0,
		   -0.0,
		   0.0,
		   -0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   1.0,
		   1.0,
		   0.0,
		   -0.0],
		  'X': 1.289125,
		  'Orden': 1,
		  'Fracción': 0.08333333333333333,
		  'Z': -1.382994127100638},
		 'BC': {'Vector': [1.0,
		   1.0,
		   -1.0,
		   -1.0,
		   -1.0,
		   -1.0,
		   1.0,
		   1.0,
		   0.0,
		   -0.0,
		   0.0,
		   -0.0,
		   0.0,
		   0.0,
		   0.0,
		   -0.0,
		   0.0,
		   0.0,
		   0.0,
		   -0.0,
		   0.0,
		   -0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   -0.0,
		   1.0,
		   1.0],
		  'X': 0.7012499999999999,
		  'Orden': 0,
		  'Fracción': -0.08333333333333333,
		  'Z': 0},
		 'ABC': {'Vector': [-1.0,
		   1.0,
		   1.0,
		   -1.0,
		   1.0,
		   -1.0,
		   -1.0,
		   1.0,
		   0.0,
		   -0.0,
		   0.0,
		   -0.0,
		   0.0,
		   -0.0,
		   0.0,
		   -0.0,
		   0.0,
		   -0.0,
		   0.0,
		   -0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0,
		   0.0],
		  'X': 0.08225000000000016,
		  'Orden': 0,
		  'Fracción': -0.07142857142857142,
		  'Z': 0},
		  'N_Datos':31}

	Planteamiento(datos, NormDist, 'base')
