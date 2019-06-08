from IPython.display import *
from ipywidgets import *

class Models():
	"""
		Imprime los modelos matemáticos planteados.
	"""
	def __init__(self, datos):
		self.Results = {}
		self.Results['Num_Ecu'] = self.Num_Ecu(datos)

		self.Imprime(datos)

	def Imprime(self, datos):
		display(Markdown(
			"""
				$$
				\begin{equation}
					x^2
				\end{equation}
				$$
			"""
			))

	def Num_Ecu(self, datos):
		cont = 1
		for key in datos:
			cont+=1
		return cont

	def __call__(self):
		return self.Results