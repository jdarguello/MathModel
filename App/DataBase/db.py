import sqlite3
import numpy as np

class varANDstr():
	"""
		Convierte las variables en texto para almacenamiento,
		y el texto en variables para procesamiento.
	"""
	def ListTEXT(self, lista):
		texto = ''
		cont = 1
		for item in lista:
			if cont < len(lista):
				ad = '\t'
			else:
				ad = ''
			cont += 1
			texto += str(item) + ad
		return texto

	def TextLIST(self, texto):
		lista = []
		for c in texto.split('\t'):
			try:
				lista.append(float(c))
			except:
				lista.append(c)
		return lista

	def MatrixTEXT(self, matrix):
		texto = ''
		cont = 1
		for lista in matrix:
			if cont < len(matrix):
				ad = '\n'
			else:
				ad = ''
			cont += 1
			texto += self.ListTEXT(lista) + ad
		return texto

	def TextMATRIX(self, texto):
		matrix = []
		for c in texto.split('\n'):
			matrix.append(self.TextLIST(c))
		return np.array(matrix)

	def TextLISTARRAY(self, texto):
		return np.array(self.TextLIST(texto))

	def DicTEXT(self, dic):
		#Sólo para diccionarios con vectores como valores
		text = ''
		for key, value in dic.items():
			text += key + ':' + self.ListTEXT(value) + '\n' 
		return text

	def TextDIC(self, texto):
		#Sólo para diccionarios con vectores como valores
		dic = {}
		for fila in texto.split('\n'):
			if fila != '':
				vec = fila.split(':')
				dic[vec[0]] = self.TextLIST(vec[1])
		return dic

class Modelo(varANDstr):
	"""
		Crea y lee modelos en la base de datos.
	"""
	def __init__(self, nombre, dic={}):
		self.info = dic
		self.nombre = nombre

		self.db = sqlite3.connect(self.nombre + '.db')

	def Create(self):
		for key in self.info:
			pass
		info = self.info[key]
		c = self.db.cursor()
		c.execute(
				"""INSERT INTO Modelos VALUES (
					:key,
					:Eq,
					:Variables,
					:Matrix,
					:Bs,
					:Ycal,
					:YiYcal,
					:YiYexpprom,
					:R2,
					:R2aju
				)""",
				{
					'key':key,
					'Eq': self.ListTEXT(info['Ecuación']),
					'Variables': self.DicTEXT(info['Variables']),
					'Matrix': self.MatrixTEXT(info['Matriz exp']),
					'Bs': self.ListTEXT(info['Bs']),
					'Ycal': self.ListTEXT(info['Ycal']),
					'YiYcal': self.ListTEXT(info['Yi-Ycal']),
					'YiYexpprom': self.ListTEXT(info['Yi-Yexpprom']),
					'R2': info['R2'],
					'R2aju': info['R2aju']
				}
			)

		self.db.commit()

	def Done(self):
		self.db.close()

	def Read(self, num):
		#Regeneración del diccionario
		try:
			int(num)
			info = self.Read_db(num)
		except:
			info = self.Read_db(num, False)
		info = info[0]

		return {
			info[0]: {
				'Ecuación': self.TextLIST(info[1]),
				'Variables': self.TextDIC(info[2]),
				'Matriz exp': self.TextMATRIX(info[3]),
				'Bs': self.TextLISTARRAY(info[4]),
				'Ycal': self.TextLISTARRAY(info[5]),
				'Yi-Ycal': self.TextLISTARRAY(info[6]),
				'Yi-Yexpprom': self.TextLISTARRAY(info[7]),
				'R2': info[8],
				'R2aju': info[9]
			}
		}

	def Read_db(self, num, number = True):
		#Lectura de la base de datos
		c = self.db.cursor()

		if number:
			c.execute("SELECT * FROM Modelos WHERE num_eq = :num", 
					{'num': num}
				)
		else:
			c.execute("SELECT * FROM Modelos WHERE Eq = :num", 
					{'num': self.ListTEXT(num)}
				)

		return c.fetchall()

class DataBase():
	"""
		Administrador de la base de datos
	"""
	def __init__(self, nombre):
		self.nombre = nombre

	def Create(self):
		db = sqlite3.connect(self.nombre + '.db')
		c = db.cursor()

		try:
			c.execute("""CREATE TABLE Modelos(
				num_eq integer,
				Eq text,
				Variables text,
				Matrix text,
				Bs text,
				Ycal text,
				YiYcal text,
				YiYexpprom text,
				R2 real,
				R2aju real
				)""")
		except:
			print('Base de datos ya creada!')

		db.commit()
		db.close()

	def Delete(self):
		pass

if __name__ == '__main__':
	name = 'data'
	pruebadb = DataBase(name)
	pruebadb.Create()

	dic = {}
	dic2 = {
		'Ecuación': ['A', 'AB'],
		'Variables': {
			'A':[-1,1,0,1],
			'AB':[1,0,0,1]
		},
		'Matriz exp': np.array([
				[-1,1,0,1],
				[1,0,0,1]
			]),
		'Bs': np.array([4.2, 5, 3.5]),
		'Ycal': np.array([3, 4, 5, 6]),
		'Yi-Ycal': np.array([2,1,4,5]),
		'Yi-Yexpprom': np.array([0,1,2,3]),
		'R2': 0.92,
		'R2aju': 0.95
	}
	dic[1] = dic2

	model = Modelo(dic= dic, nombre=name)
	#model.Create()
	print(model.Read(num=['A', 'AB']))
	model.Done()
