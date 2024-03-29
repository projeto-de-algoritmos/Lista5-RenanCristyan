import numpy

# Retorna a matriz de subproblemas completa
def initialize_matrix(x, y, gap, msmt):
	x = process_string(x)
	y = process_string(y)

	m = len(y) 
	n = len(x) 

	matrix = numpy.zeros((m, n))

	for i in range(m):
		matrix[i][0] = i*gap

	for j in range(n):
		matrix[0][j] = j*gap

	i, j = 1, 1
	while i < m:
		j = 1
		while j < n:
			if x[j] == y[i]:
				msm = 0
			else:
				msm = msmt

			option1 = msm + matrix[i-1][j-1]
			option2 = gap + matrix[i-1][j]
			option3 = gap + matrix[i][j-1]

			matrix[i][j] = min(option1, option2, option3)
			j += 1
		i += 1

	return matrix

# Imprime a melhor sequencia encontrada **de baixo para cima**
def find_sequence(matrix, x, y, gap, msmt, i, j):
	if x[j-1] == y[i-1]:
		msm = 0
	else:
		msm = msmt

	option1 = msm + matrix[i-1][j-1]
	option2 = gap + matrix[i-1][j]
	option3 = gap + matrix[i][j-1]
	minimum = min(option1, option2, option3)

	if i == 0 and j == 0:
		return

	elif minimum == option1:
		print('{}-{}'
			  .format(x[j-1], y[i-1]))
		find_sequence(matrix, x, y, gap, msmt, i-1, j-1)
	
	elif minimum == option2:
		print('_-{}'
			  .format(y[i-1]))
		find_sequence(matrix, x, y, gap, msmt, i-1, j)
	
	else:
		print('{}-_'
			  .format(x[j-1]))
		find_sequence(matrix, x, y, gap, msmt, i, j-1)

# Imprime a melhor sequencia encontrada de forma mais elegante
# do que a versão recursiva (e na ordem correta)
def iterative_find_sequennce(matrix, x, y, gap, msmt):
	i = len(matrix) - 1
	j = len(matrix[0]) - 1

	x_list = []
	y_list = []

	while True:
		if i == 0 and j == 0:
			break

		if i <= 1 or j <= 1:
			msm = msmt
		
		else:	
			if x[j-1] == y[i-1]:
				msm = 0
			else:
				msm = msmt

		option1 = msm + matrix[i-1][j-1]
		option2 = gap + matrix[i-1][j]
		option3 = gap + matrix[i][j-1]
		minimum = min(option1, option2, option3)

		if minimum == option1:
			x_list.append(x[j-1])
			y_list.append(y[i-1])
			i -= 1
			j -= 1
		elif minimum == option2:
			x_list.append('-')
			y_list.append(y[i-1])
			i -= 1
		else:
			x_list.append(x[j-1])
			y_list.append('-')
			j -= 1

	separator = ''
	print('X =', separator.join(x_list[::-1]))
	print('Y =', separator.join(y_list[::-1]))

# Retorna o melhor valor, ou seja, o último elemento da matriz
def best_value(matrix):
	l = len(matrix) - 1
	c = len(matrix[0]) - 1

	return matrix[l][c]

# Retorna uma lista de caracteres da string
def process_string(string):
	p_string = [0]
	for l in string:
		p_string.append(l)
	return p_string

# Executa as funções auxiliares e exibe o resultaado
def run(x, y, gap, msmt, show_matrix=False):
	print('_'*50)

	print('X = {}'.format(x))
	print('Y = {}'.format(y))
	print('GAP = {}'.format(gap))
	print('MISMATCH = {}'.format(msmt))

	matrix = initialize_matrix(x, y, gap, msmt)

	if show_matrix:
		print('\nMatriz de subproblemas: ')
		print(matrix)

	melhor_valor = best_value(matrix)

	print('\nMelhor alinhamento com {} pontos:'
		    .format(melhor_valor))

	iterative_find_sequennce(matrix, x, y, gap, msmt)

	print('_'*50)

# Alguns exemplos
run('CTACCG', 'TACATG', 2, 3)
run('TAG', 'AGT', 1, 2)
run('ATCGGA', 'ATGC', 2, 3, show_matrix=True)
run('STOP', 'TOPS', 1, 2)
run('ATA', 'TATAT', 1, 2, show_matrix=True)
run('GGGGCCCCCGGGG', 'GCG', 1, 2, show_matrix=True)
run('A', 'TTTGCACGTTT', 2, 3, show_matrix=True)