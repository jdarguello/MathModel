def Factorial(n):
	producto = 1
	for i in range(n):
		producto *= (n-i)
	return producto
print(Factorial(23))