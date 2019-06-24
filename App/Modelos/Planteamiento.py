import numpy as np
import itertools as it
import math
import gc


#from App.DataBase.db import *

class Planteamiento():
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
			
	def Calculos(self, Ecu, datos, NormDist, nombre):
		cont = self.contador
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
		#self.Guardar(dic, nombre)
		self.contador += 1
		self.Mejores[cont] = dic[cont]

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

		for i in range(len(Efecto)):
			Ecu = list(it.combinations(Efecto, i+1))
			for Ec in Ecu:
				self.Calculos(Ec, datos, NormDist, nombre)
			#print(self.Mejores)

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