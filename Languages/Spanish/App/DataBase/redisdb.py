import redis
import json
import numpy as np

class Red():
	"""
		Almacenar y leer diccionarios
	"""

	def __init__(self):
		self.conn = redis.Redis('localhost')

	def Write(self, dic):
		#dic = {'name':'algo', 'number':123}
		self.conn.hmset('1', json.dumps(dic))

	def Read(self):
		dic = self.conn.hgetall('1')

if __name__ == '__main__':
	dic = {
		'Ecuación':['A', 'AB'],
		'Variables': {
			'A':[1,1,1],
			'AB':[0,0,0]
		},
		'Matriz exp':np.array(
				[
					[1,1,1],
					[0,0,0]
				]
			).tolist(),
		'Ycal': np.array([0.2, 0.1, 0.1]).tolist(),
		'R2': 0.5
	}
	db = Red()
	db.Write(dic)
	#db.Read()