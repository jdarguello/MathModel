import numpy as np
import IPython.display as IP

def combinations(iterable, r):
	pool = tuple(iterable)
	n = len(pool)
	if r > n:
		return
	indices = list(range(r))
	cont = 1
	while True:
		Ec = list(pool[i] for i in indices)
		print(Ec, cont)
		for i in reversed(range(r)):
			if indices[i] != i + n - r:
				break
		else:
			return
		indices[i]  += 1
		
		for j in range(i+1, r):
			indices[j] = indices[j-1] + 1
		cont += 1

if __name__ == '__main__':
	#print(combinations(['A', 'B', 'C', 'AB', 'AC', 'BC', 'ABC'], 2))

	x = np.array([1,1,1])
	y = np.array([0,2,0])
	z = [i for i in range(len(x))]
	print(IP.__file__)
