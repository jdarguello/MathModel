import numpy as np

from App.Modelos.Planteamiento import ModelosIniciales

class AleatoriedadY(ModelosIniciales):
	"""
		Prueba de aleatoriedad Y para validar el modelo propuesto.
	"""
	def __init__(self, Modelo, Y, Estab, nombre):
		self.Respuesta = []
		self.Valid(Modelo, Y, nombre, Estab)

	def Valid(self, Modelo, Y, nombre, Estab):
		R2_ref = Modelo['R2aju']
		R2_cal = 0
		R2_val = 0
		matrix_or = Modelo['Matriz exp']
		exp = self.Exponentes(Modelo['Ecuación'])
		while R2_val < R2_ref or R2_cal < R2_ref:
			matriz = np.c_[matrix_or, Y]
			np.random.shuffle(matriz)
			M = self.CalVal(Modelo['Ecuación'], \
				nombre, exp, Estab, matrix=matriz)

			if M is not None:
				R2_val = M['R2_val']
				R2_cal = M['R2_cal']
				self.Respuesta.append(M)

	def CalVal(self, Ecu, nombre, exponentes, Estab, matrix):
		#Partición Ys
		matriz_cal = []
		Y_calc = []
		matriz_val = []
		Y_val = []
		for i in range(int(round(len(matrix[:,len(Ecu)+1:])))):
			if i <= 0.6*(round((len(matrix[:,len(Ecu)+1:]))) - 1):
				Y_calc.append(matrix[i][len(Ecu)+1])
				matriz_cal.append(matrix[i][:])
			else:
				Y_val.append(matrix[i][len(Ecu)+1])
				matriz_val.append(matrix[i][:])
		matriz_cal = np.array(matriz_cal)
		matriz_val = np.array(matriz_val)

		Modelo_cal = self.Calculos(Ecu, np.array(matriz_cal[:,len(Ecu)+1:]),\
		 {'N_Datos': len(Y_calc)}, nombre, exponentes, matrix = matriz_cal[:,:-1], matrixx = True)

		Modelo_val = self.Calculos(Ecu, np.array(matriz_val[:,len(Ecu)+1:]),\
		 {'N_Datos': len(Y_val)}, nombre, exponentes, matrix = matriz_val[:,:-1], matrixx = True)

		if Modelo_cal is not None and Modelo_val is not None:
			Modelo = {}
			Modelo['Bs'] = Modelo_cal['Bs']
			suma_calc_residuo = 0
			suma_val_residuo = 0
			for i in range(int(round(len(matrix[:,len(Ecu)+1:])))):
				if i <= 0.6*(round((len(matrix[:,len(Ecu)+1:]))) - 1):
					suma_calc_residuo += Modelo_cal['Yi-Ycal'][i]**2
					j = 0
				else:
					suma_val_residuo += Modelo_val['Yi-Ycal'][j]**2
					j += 1
			Modelo['Y_calc'] = np.array(Y_calc)
			Modelo['Y_val'] = np.array(Y_val)
			Modelo['Ypromcalc'] = np.mean(np.array(Y_calc))
			Modelo['Ypromval'] = np.mean(np.array(Y_val))
			Modelo['suma_cua_val_residuo'] = suma_val_residuo
			Modelo['suma_cua_calc_residuo'] = suma_calc_residuo

			suma_calc_y_yprom = 0
			suma_val_y_yprom = 0
			for i in range(int(round(len(matrix[:,len(Ecu)+1:])))):
				if i <= 0.6*(round((len(matrix[:,len(Ecu)+1:]))) - 1):
					suma_calc_y_yprom += (matrix[i][len(Ecu)+1]-Modelo['Ypromcalc'])**2
					j = 0
				else:
					suma_val_y_yprom += (matrix[j][len(Ecu)+1]-Modelo['Ypromval'])**2
					j += 1

			Modelo['suma_cua_val_y_yprom'] = suma_val_y_yprom
			Modelo['suma_cua_calc_y_yprom'] = suma_calc_y_yprom

			#Validación
			Modelo['R2_cal'] = (Modelo['suma_cua_calc_y_yprom']-Modelo['suma_cua_calc_residuo'])/Modelo['suma_cua_calc_y_yprom']
			Modelo['R2_val'] = (Modelo['suma_cua_val_y_yprom']-Modelo['suma_cua_val_residuo'])/Modelo['suma_cua_val_y_yprom']
			Modelo['RMSEC'] = (Modelo['suma_cua_calc_residuo']/(len(Y_calc)-len(Ecu)-1))**(1/2)
			Modelo['RMSEP'] = (Modelo['suma_cua_val_residuo']/(len(Y_val))**(1/2))
			Modelo['SSRES'] = Modelo['suma_cua_val_residuo'] + Modelo['suma_cua_calc_residuo']
			Modelo['Error_Exp'] = Estab['Varianza']*len(matrix[:,len(Ecu)+1:])
			Modelo['LOF'] = Modelo['SSRES']-Modelo['Error_Exp']
			return Modelo

	def Exponentes(self, Ecu):
		exp = []
		for i in range(len(Ecu)):
			val = ''
			for j in range(len(Ecu[i])):
				try:
					exponentes.append(int(Ecu[i][j]))
				except:
					pass
		return exp