import numpy as np

from App.Modelos.Planteamiento import ModelosIniciales

class AleatoriedadY(ModelosIniciales):
	"""
		Prueba de aleatoriedad Y para validar el modelo propuesto.
	"""
	def __init__(self, Modelo, Y):
		self.Respuesta = {}
		self.Inicial(Modelo, Y)

	def Inicial(self, Modelo, Y):
		pass

	def CalVal(self, Ecu, Y, Y_real NormDist, nombre, exponentes):
		Modelo =  self.Calculos(Ecu, Y, NormDist, nombre, exponentes)

		#Partición Ys
		Y_calc = []
		suma_calc_residuo = 0
		Y_val = []
		suma_val_residuo = 0
		for i in range(int(len(Y))/2):
			if i <= int(len(Y)/2) - 1:
				Y_calc.append(Y[i])
				suma_calc_residuo += Modelo['Yi-Ycal'][i]**2
			else:
				Y_val.append(Y[i])
				suma_val_residuo += Modelo['Yi-Ycal'][i]**2

		Modelo['Y_calc'] = np.array(Y_calc)
		Modelo['Y_val'] = np.array(Y_val)
		Modelo['Ypromcalc'] = np.mean(np.array(Y_calc))
		Modelo['Ypromval'] = np.mean(np.array(Y_val))
		Modelo['suma_cua_val_residuo'] = suma_val_residuo
		Modelo['suma_cua_calc_residuo'] = suma_calc_residuo

		suma_calc_y_yprom = 0
		suma_val_y_yprom = 0
		for i in range(int(len(Y))/2):
			if i <= int(len(Y)/2) - 1:
				Y_calc.append(Y[i])
				suma_calc_y_yprom += (Y_real[i]-Modelo['Ypromcalc'])**2
			else:
				Y_val.append(Y[i])
				suma_val_y_yprom += (Y_real[i]-Modelo['Ypromval'])**2

		Modelo['suma_cua_val_y_yprom'] = suma_val_y_yprom
		Modelo['suma_cua_calc_y_yprom'] = suma_calc_y_yprom

		#Validación
		Modelo['R2_cal'] = (Modelo['suma_cua_calc_y_yprom']-Modelo['suma_cua_calc_residuo'])/Modelo['suma_cua_calc_y_yprom']
		Modelo['R2_val'] = (Modelo['suma_cua_val_y_yprom']-Modelo['suma_cua_val_residuo'])/Modelo['suma_cua_val_y_yprom']
		Modelo['RMSEC'] = (Modelo['suma_cua_calc_residuo']/(len(Y_real)-len(Ecu)-1))**(1/2)
		Modelo['RMSEP'] = (Modelo['suma_cua_val_residuo']/(len(Y_real)-len(Ecu)))**(1/2)
		Modelo['SSRES'] = Modelo['suma_cua_val_residuo'] + Modelo['suma_cua_calc_residuo']
		Modelo['Error_Exp'] = 0
		Modelo['LOF'] = Modelo[]

	def Valid(self, Modelo):
		pass

	def Random(self):
		pass