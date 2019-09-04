import csv
import os

class Save():
	"""
		Guarda la información en un archivo .csv
	"""
	def __init__(self, current_dir, Modelo, ValData, Y, filename):
		self.ruta = current_dir + '/App/DataBase/Resultados/'
		self.CrearDic(filename)
		self.Guarda(Modelo, ValData, Y, filename)

	def CrearDic(self, filename):
		try:
			os.mkdir(self.ruta + filename)
		except:
			pass
		self.ruta += filename + '/'

	def Guarda(self, Modelo, ValData, Y, filename):
		def Info():
			with open(csv_file, 'w') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
				writer.writeheader()
				for data in dict_data:
					writer.writerow(data)
		#Modelo Matemático
		csv_file = self.ruta + 'MathModel' + '.csv'
		csv_columns, dict_data = self.ModeloMat(Modelo, Y)
		Info()
		
		#Validación
		csv_file = self.ruta + 'Validation' + '.csv'
		csv_columns, dict_data = self.Validation(ValData)
		Info()

	def Validation(self, ValData):
		#Nombre de columnas
		csv_columns = []
		for key in ['R2_cal', 'R2_val', 'RMSEC', 'RMSEP', 'LOF']:
			csv_columns.append(key)
		for i in range(len(ValData[0]['Bs'])):
			csv_columns.append('B' + str(i))

		#Contenido
		dic_data = []
		for i in range(len(ValData)):
			dic = {}
			for item in ['R2_cal', 'R2_val', 'RMSEC', 'RMSEP', 'LOF']:
				dic[item] = round(ValData[i][item],3)
			for j in range(len(ValData[i]['Bs'])):
				dic['B' + str(j)] = round(ValData[i]['Bs'][j],3)
			dic_data.append(dic)

		return csv_columns, dic_data
		
	def ModeloMat(self, Modelo, Y):
		#Nombre de columnas
		csv_columns = []
		for key in Modelo['Ecuación']:
			csv_columns.append(key)
		for item in ['Y', 'Ycal', 'Yi-Ycal', 'Yi-Yexpprom']:
			csv_columns.append(item)

		#Contenido
		dic_data = []
		for i in range(len(Y)):
			dic = {}
			for key in Modelo['Variables']:
				dic[key] = Modelo['Variables'][key]['Vector'][i]
			dic['Y'] = Y[i]
			for item in ['Ycal', 'Yi-Ycal', 'Yi-Yexpprom']:
				dic[item] = round(Modelo[item][i],4)
			dic_data.append(dic)

		return csv_columns, dic_data