from IPython.display import HTML, display
import numpy as np

class Models():
	"""
		Imprime los modelos matemáticos planteados.
	"""
	def __init__(self, resultado):
		self.Equation(resultado)
		self.R2aju(resultado)

	def Equation(self, res):
		texto = 'Y = \\beta_0'
		cont = 1
		for Ec in res['Ecuación']:
			texto += ' + \\beta _{' + str(cont) + '}'
			cont += 1
			for E in Ec:
				texto += E
				if res['Variables'][Ec]['Exponentes'][E] != 1.0:
					texto += '^{' + str(res['Variables'][Ec]['Exponentes'][E]) + '}'
		texto += '\\rightarrow \\left[\\beta _{' + str(0) + '}'
		cont = 1
		for Ec in res['Ecuación']:
			texto += ', \\beta _{' + str(cont) + '}'
			cont += 1
		texto += '\\right] = \\left['
		cont = 1
		for B in res['Bs']:
			if cont < len(res['Bs']):
				fin = ', '
			else:
				fin = ''
			texto += str(round(B,3)) + fin
			cont += 1
		texto += '\\right]'
		self.Imprime('$' + texto + '$')

	def R2aju(self, res):
		texto = 'R ^2 _{ajus} = ' + str(round(res['R2aju'],3))
		self.Imprime('$' + texto + '$')

	def Imprime(self, texto):
		display(HTML(texto))

if __name__ == '__main__':
	res = {
		'Ecuación': ('AB', 'B', 'C'),
		'Variables': {
			'AB': {
				'Exponentes': {'A':1.0, 'B':1.0}
			},
			'B':{'Exponentes':{'B':1.0}},
			'C':{'Exponentes':{'C':1.0}}
		},
		'R2aju': 0.34,
		'Bs': np.array([3.901, 1,763, 0.96027, 0.84387])
	}
	Models(res)