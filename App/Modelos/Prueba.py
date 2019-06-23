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

import numpy as np

if __name__ == '__main__':
	#print(combinations(['A', 'B', 'C', 'AB', 'AC', 'BC', 'ABC'], 2))

	x = np.array(
		[('A', 7.5625), ('B', 1.890625)], 
		dtype=[('comb', 'U10'), ('par', 'f4')])
	print(tuple(('x',2)))
	print(np.sort(x, order='par'))