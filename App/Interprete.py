import os
import pandas as pd

class Data():
	"""
		Interpretar los datos experimentales de la base de datos
	"""
	ext = '.txt'
	anterior = os.path.dirname(os.path.realpath(__file__))
	def __init__(self, archivo, kind=True):
		self.datos = {}
		if kind:
			start = 'App/Database/Datos/'
		else:
			start = 'Database/Datos/'
		data = self.Read(start + archivo + \
			self.ext)
		self.Process(data)

	def Process(self, info):
		for var in list(info):
			self.datos[var] = []

		for row in info.values:
			cont = 0
			for key in self.datos:
				if isinstance(row[cont], str):
					self.datos[key].append(float(row[cont].replace(',', '.')))
				else:
					self.datos[key].append(row[cont])
				cont += 1

	def Read(self, file):
		data = pd.read_csv(file, sep="\t")
		return pd.DataFrame(data)

	def __call__(self):
		return self.datos

if __name__ == '__main__':
	D = Data('2', kind=False)()
	print(D)