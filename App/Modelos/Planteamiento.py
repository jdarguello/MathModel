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
	def __init__(self, Ecuacion, NormDist, Y, maximo = 3):
		self.Respuestas = {}
		self.Ans = {}
		self.CombExp(Ecuacion, NormDist, Y, maximo)

	def CombExp(self, Ecuacion, NormDist, Y, maximo):
		#Exponentes
		contador = 0
		for i in range(len(Ecuacion)):
			for E in Ecuacion[i]:
				contador += 1
		exponentes = np.ones(contador)

		#Ecuaciones
		cont = 1
		for i in range(contador):
			for j in range(maximo):
				exponentes[i] = j+1
				self.Respuestas[cont] = self.Calculos(Ecuacion, Y, NormDist, '', \
					exponentes)
				cont += 1

if __name__ == '__main__':
	datos = {
		'A':[1,1,1],
		'B': [0,0,0],
		'C': [1,1,1],
		'D': [0,0,0],
	}
	Efecto = ('AB', 'C', 'B')
	NormDist = {}
	Planteamiento(datos, NormDist, Efecto, 'base')

	exponentes = [1, 1, 1, 1]