import numpy as np
import itertools as it

class Planteamiento():
	"""
		Plantear la mayoría, por lo menos,
		de los modelos matemáticos posibles.
	"""

	def __init__(self, datos):
		pass

def Factorial(n):
	producto = 1
	for i in range(n):
		producto *= (n-i)
	return producto

if __name__ == '__main__':
	datos = {
		'A': [1,0,-1,1],
		'B': [1,-1,1,0],
		'Y': [0.6, 0.8, 0.7, 1.2]
	}
	Planteamiento(datos)
	n = 3
	print((n+1)*Factorial(n)+1)