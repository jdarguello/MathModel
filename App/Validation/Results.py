from IPython.display import HTML, display

class TablaAlY():
	"""
		Imprime los resultados de la prueba de aleatoriedad - Y.
	"""
	def __init__(self, data, Ecu):
		Res = self.Data(data, Ecu)
		self.Res(Res)

	def Data(self, data, Ecu):
		Base = ['$ R ^2 _{cal} $', '$ R^2 _{val} $', '$RMSEC$', '$RMSEP$', '$LOF$']
		for i in range(len(Ecu)+1):
			Base.append('$' + '\\beta _' + str(i) + ' $')
		Res = []
		Res.append(Base)
		for i in range(len(data)):
			lista = []
			for item in ['R2_cal', 'R2_val', 'RMSEC', 'RMSEP', 'LOF']:
				lista.append(round(data[i][item],3))
			for B in data[i]['Bs']:
				lista.append(round(B,3))
			Res.append(lista)
		return Res

	def Res(self, data):
		display(HTML(
		   '<table><tr>{}</tr></table>'.format(
		       '</tr><tr>'.join(
		           '<td>{}</td>'.format('</td><td>'.join(str(_) for _ in row)) for row in data)
		       )
		))
