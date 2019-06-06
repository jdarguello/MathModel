import os
import pandas as pd

class Data():
	"""
		Interpretar los datos experimentales de la base de datos
	"""
	datos = {}
	ext = '.txt'
	anterior = os.path.dirname(os.path.realpath(__file__))
	def __init__(self, archivo):
		data = self.Read('App/Datos/' + archivo + \
			self.ext)
		self.Process(data)

	def Process(self, info):
		for var in list(info):
			self.datos[var] = []

		for row in info.values:
			cont = 0
			for key in self.datos:
				self.datos[key].append(float(row[cont].replace(',', '.')))
				cont += 1

	def Read(self, file):
		data = pd.read_csv(file, sep="\t")
		return pd.DataFrame(data)

	def __call__(self):
		return self.datos

if __name__ == '__main__':
	Data('1')