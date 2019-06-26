import numpy as np
import itertools as it
import math
import gc


#from App.DataBase.db import *

class ModelosIniciales():
	"""
		Plantear los modelos matemáticos iniciales y escoger
		el de mayor efecto.
	"""

	def __init__(self, datos, NormDist, Efecto, nombre):
		self.Mejores = {}
		self.contador = 1
		#Creación base de datos
		"""
		nombre = 'App/DataBase/' + nombre
		BD = DataBase(nombre)
		BD.Create()
		"""

		#Llenado de la base de datos
		self.Combinaciones(datos, Efecto, NormDist, nombre)

		self.Selection()

	def Selection(self):
		Rmax = 0
		for key in self.Mejores:
			if self.Mejores[key]['R2aju'] > Rmax:
				Rmax = self.Mejores[key]['R2aju']
				self.Mejor = self.Mejores[key]
			
	def Calculos(self, Ecu, Y, NormDist, nombre, exponentes):
		dic = {
			'Ecuación':Ecu,
			'Variables': {}
		}
		M = []
		M.append(np.ones(NormDist['N_Datos']))
		contador = 0
		for i in range(len(Ecu)):
			dic['Variables'][Ecu[i]] = {}
			subdic= {
				'Exponentes': {},
				'Vector': np.ones(NormDist['N_Datos'])
			}
			for Ec in Ecu[i]:
				subdic['Exponentes'][Ec] = exponentes[contador]
				for k in range(int(exponentes[contador])):
					subdic['Vector'] *= NormDist[Ec]['Vector']
				contador += 1
			dic['Variables'][Ecu[i]] = subdic
			M.append(dic['Variables'][Ecu[i]]['Vector'])
		dic['Matriz exp'] = np.transpose(np.array(M))
		dic['Bs'] = np.matmul(
			np.matmul(
				np.linalg.inv(np.matmul(
					np.transpose(dic['Matriz exp']),
					dic['Matriz exp']
					)),
				np.transpose(
					dic['Matriz exp'])), 
			np.transpose(Y)
			)
		dic['Ycal'] = np.matmul(
			dic['Matriz exp'],
			dic['Bs']
			)
		#Yi - Ycal, Yi - Yexpprom
		dic['Yi-Ycal'] = np.zeros(NormDist['N_Datos'])
		dic['Yi-Yexpprom'] = np.zeros(NormDist['N_Datos'])
		for i in range(NormDist['N_Datos']):
			dic['Yi-Ycal'][i] = \
				Y[i] - dic['Ycal'][i]
			dic['Yi-Yexpprom'][i] = \
				Y[i] - np.mean(Y)
		SSreg = np.sum(dic['Yi-Ycal']**2)
		SStot = np.sum(dic['Yi-Yexpprom']**2)
		dic['R2'] = (SStot-\
				SSreg)/SStot
		dic['R2aju'] = \
			(SStot/(NormDist['N_Datos']-1)-\
				SSreg/(NormDist['N_Datos']-\
					len(dic['Ecuación'])-\
					1))/(SStot/(NormDist['N_Datos']-1))
		#self.Guardar(dic, nombre)
		return dic

	def Guardar(self, dic, nombre):
		model = Modelo(nombre, dic)
		model.Create()

	def Combinaciones(self, datos, Efecto, NormDist, nombre):
		"""
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
		print(combinaciones)

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

		#Ecu_ant = []
		for i in range(Total_Var):
			#self.combinations(combs, i+1, datos, NormDist, nombre)
			Ecu = list(it.combinations(combs, i+1))
			print(Ecu)
		"""
		cont = 1
		for i in range(len(Efecto)):
			Ecu = list(it.combinations(Efecto, i+1))
			for Ec in Ecu:
				contador = 0
				for i in range(len(Ec)):
					for E in Ec[i]:
						contador += 1
				exponentes = np.ones(contador)
				dic = self.Calculos(Ec, datos['Y'], NormDist, nombre, exponentes)
				self.Mejores[cont] = dic
				cont += 1

	def combinations(self, iterable, r, datos, NormDist, nombre):
		pool = tuple(iterable)
		n = len(pool)
		if r > n:
			return
		indices = list(range(r))
		while True:
			Ec = list(pool[i] for i in indices)
			self.Calculos(Ec, datos, NormDist, nombre)
			#print(Ec)
			del Ec
			for i in reversed(range(r)):
				if indices[i] != i + n - r:
					break
			else:
				gc.collect()
				return
			indices[i]  += 1
			
			for j in range(i+1, r):
				indices[j] = indices[j-1] + 1


	def __call__(self):
		return self.Mejores

class ModeloFinal(ModelosIniciales):
	"""
		A partir del mejor modelo inicial, se desarrolla un proceso iterativo
		que permita seleccionar los exponentes finales.
	"""
	def __init__(self, Ecuacion, NormDist, Y = None, maximo = 3):
		self.Respuestas = {}
		self.Ans = {}
		self.CombExp(Ecuacion, NormDist, Y, maximo)
		#self.Selection()

	def CombExp(self, Ecuacion, NormDist, Y, maximo):
		#Exponentes
		contador = 0
		for i in range(len(Ecuacion)):
			for E in Ecuacion[i]:
				contador += 1
		exponentes = np.ones(contador)

		comb = {}
		for Ec in Ecuacion:
			comb[Ec] = []
			cont = np.ones(len(Ec))
			ultimo = len(Ec)-1
			while ultimo != -1:
				var = ''
				for i in range(len(Ec)):
					if i == len(Ec)-1:
						for j in range(maximo):
							comb[Ec].append(var + Ec[i] + str(int(cont[i])))
							cont[i] += 1
						cont[i] = 1
						var = ''
						if cont[ultimo] == maximo or ultimo == len(Ec)-1:
							ultimo -= 1
						cont[ultimo] += 1
						var = ''
					else:
						var += Ec[i] + str(int(cont[i]))	

		#c = list(it.combinations(dic, len(Ec)))
		print(comb)

		#Ecuaciones
		"""
		cont = 1
		for Ec in Ecuacion:
			if len(Ec) > 1:

		combinaciones = list(it.combinations(comb, len(Ecuacion)))
		for c in combinaciones:
			self.Respuestas[cont] = self.Calculos(Ecuacion, Y, NormDist, '', \
				exponentes)
			cont += 1
		"""

	def Selection(self):
		Rmax = 0
		for key in self.Respuestas:
			if self.Respuestas[key]['R2aju'] > Rmax:
				self.Ans = self.Respuestas[key]
				Rmax = self.Respuestas[key]['R2aju']

if __name__ == '__main__':
	Eq = ('A','AB','C')
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
	   2.0,
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
	  'X': 5.1937500000000005,
	  'Orden': 6,
	  'Fracción': 0.7857142857142857,
	  'Z': 0.7916386077433746},
	 'B': {'Vector': [-1.0,
	   -1.0,
	   1.0,
	   1.0,
	   -1.0,
	   -1.0,
	   1.0,
	   1.0,
	   0.0,
	   2.0,
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
	  'X': 2.322625,
	  'Orden': 3,
	  'Fracción': 0.35714285714285715,
	  'Z': -0.36610635680056963},
	 'C': {'Vector': [-1.0,
	   -1.0,
	   -1.0,
	   -1.0,
	   1.0,
	   1.0,
	   1.0,
	   1.0,
	   2.0,
	   0.0,
	   0.0,
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
	  'X': 3.095625,
	  'Orden': 4,
	  'Fracción': 0.5,
	  'Z': 0.0},
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
	  'Orden': 5,
	  'Fracción': 0.6428571428571429,
	  'Z': 0.3661063568005698},
	 'AC': {'Vector': [1.0,
	   -1.0,
	   1.0,
	   -1.0,
	   -1.0,
	   1.0,
	   -1.0,
	   1.0,
	   0.0,
	   0.0,
	   0.0,
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
	  'Orden': 2,
	  'Fracción': 0.21428571428571427,
	  'Z': -0.7916386077433746},
	 'BC': {'Vector': [1.0,
	   1.0,
	   -1.0,
	   -1.0,
	   -1.0,
	   -1.0,
	   1.0,
	   1.0,
	   0.0,
	   0.0,
	   0.0,
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
	  'Orden': 1,
	  'Fracción': 0.07142857142857142,
	  'Z': -1.465233792685523},
	 'ABC': {'Vector': [-1.0,
	   1.0,
	   1.0,
	   -1.0,
	   1.0,
	   -1.0,
	   -1.0,
	   1.0,
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
	   0.0,
	   0.0,
	   0.0,
	   0.0],
	  'X': 0.08225000000000016,
	  'Orden': 0,
	  'Fracción': -0.07142857142857142,
	  'Z': 0},
	 'N_Datos': 22}
 	
	ModeloFinal(Eq, NormDist)
