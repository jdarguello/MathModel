import numpy as np
import itertools as it
import math

class Planteamiento():
	"""
		Plantear la mayoría de los modelos matemáticos posibles.
	"""

	def __init__(self, datos, NormDist):
		self.Planteamiento = {}
		self.Mejores = {}
		Ecu = self.Combinaciones(datos, NormDist)
		self.Calculos(Ecu, datos, NormDist)
		self.Selection()

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
			

	def Calculos(self, Ecu, datos, NormDist):
		#SE PUEDE ARREGLAR, ES SÓLO CAMBIAR for Ec in Ecu, adaptarlo al otro
		cont = 1
		for Ec in Ecu:
			for Equation in Ec:
				self.Planteamiento[cont] = {
					'Ecuación':[],
					'Variables': {}
				}
				M = []
				onevec = []
				for i in range(NormDist['N_Datos']):
					onevec.append(1)
				M.append(onevec)
				for i in range(len(Equation)):
					self.Planteamiento[cont]['Ecuación'].append(Equation[i])
					self.Planteamiento[cont]['Variables'][Equation[i]] = \
						NormDist[Equation[i]]['Vector']
					M.append(NormDist[Equation[i]]['Vector'])
				self.Planteamiento[cont]['Matriz exp'] = np.transpose(np.array(M))
				self.Planteamiento[cont]['Bs'] = np.matmul(
					np.matmul(
						np.linalg.inv(np.matmul(
							np.transpose(self.Planteamiento[cont]['Matriz exp']),
							self.Planteamiento[cont]['Matriz exp']
							)),
						np.transpose(
							self.Planteamiento[cont]['Matriz exp'])), 
					np.transpose(datos['Y'])
					)
				self.Planteamiento[cont]['Ycal'] = np.matmul(
					self.Planteamiento[cont]['Matriz exp'],
					self.Planteamiento[cont]['Bs']
					)

				#Yi - Ycal, Yi - Yexpprom
				self.Planteamiento[cont]['Yi-Ycal'] = np.zeros(NormDist['N_Datos'])
				self.Planteamiento[cont]['Yi-Yexpprom'] = np.zeros(NormDist['N_Datos'])
				for i in range(NormDist['N_Datos']):
					self.Planteamiento[cont]['Yi-Ycal'][i] = \
						datos['Y'][i] - self.Planteamiento[cont]['Ycal'][i]
					self.Planteamiento[cont]['Yi-Yexpprom'][i] = \
						datos['Y'][i] - np.mean(datos['Y'])
				SSreg = np.sum(self.Planteamiento[cont]['Yi-Ycal']**2)
				SStot = np.sum(self.Planteamiento[cont]['Yi-Yexpprom']**2)
				self.Planteamiento[cont]['R2'] = (SStot-\
						SSreg)/SStot
				self.Planteamiento[cont]['R2aj'] = \
					(SStot/(NormDist['N_Datos']-1)-\
						SSreg/(NormDist['N_Datos']-\
							len(self.Planteamiento[cont]['Ecuación'])-\
							1))/(SStot/(NormDist['N_Datos']-1))
				cont += 1

	def Combinaciones(self, datos, NormDist):
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

		Ecu = []
		for i in range(Total_Var):
			Ecu.append(list(it.combinations(\
					combs, i+1)))
		return Ecu

	def __call__(self):
		return self.Planteamiento, self.Mejores

def nCr(n,r):
    f = math.factorial
    return f(n) // f(r) // f(n-r)

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

	Planteamiento(datos, NormDist)
