import numpy

class Knapsack():
	def __init__(self):
		self.items = []
		self.values = []
		self.weights = []

	def setItems(self, items):
		self.items.append(0)
		self.items += items

	def setValues(self, values):
		self.values.append(0)
		self.values += values

	def setWeights(self, weights):
		self.weights.append(0)
		self.weights += weights

	def setMaxWeight(self, max_weight):
		self.max_weight = max_weight

	def showKnapsack(self):
		print("itens = ", self.items)
		print("valores = ", self.values)
		print("pesos = ", self.weights)
		print("capacidade = ", self.max_weight)

	def showPrettyKnapsack(self):
		print('item\tvalor\tpeso')
		
		i = 1
		while i < len(self.items):
			print('{}\t| {}\t| {}'
				  .format(self.items[i],
				  	      self.values[i],
				  	      self.weights[i]))
			i += 1
		print('capacidade = {}'.format(self.max_weight))

# Inicializa a matriz dos subproblemas
def initialize_knapsack_matrix(knapsack):
	l = len(knapsack.items)
	c = 1 + knapsack.max_weight

	matrix = numpy.zeros((l, c))

	i = 1
	j = 1

	while i < l:
		j = 1
		while j < c:
			matrix[i][j] = -1
			j += 1
		i += 1

	return matrix

# Retorna a matriz completa dos subproblemas
def complete_matrix(knapsack):
	m = initialize_knapsack_matrix(knapsack)
	l = len(m)
	c = len(m[0])

	i = 0
	w = 0
	while i < l:
		w = 0
		while w <= knapsack.max_weight:
			m[i][w] = opt(knapsack, m, i, w)
			w += 1
		i += 1

	return m

# Retorna o último elemento da matriz, ou seja, o melhor valor obtido
def best_value(matrix):
	l = len(matrix) - 1
	c = len(matrix[0]) - 1
	
	return matrix[l][c]

# Retorna o valor correto para se preencher na matriz
def opt(knapsack, matrix, i, w):
	vi = knapsack.values[i]
	wi = knapsack.weights[i]

	if matrix[i][w] == 0:
		return 0
	elif wi > w:
		return matrix[i-1][w]
	else:
		return max(matrix[i-1][w], vi+matrix[i-1][w-wi])

# Imprime os itens que vão na mochila
def find(knapsack, matrix, i, j):
	if matrix[i][j] == 0:
		return
	elif matrix[i][j] > matrix[i-1][j]:
		print(i)
		find(knapsack, matrix, i-1, j-knapsack.weights[i])
	else:
		find(knapsack, matrix, i-1, j)

# Executa as funções auxiliares e mostra o resultado final
def run(knapsack):
	print('-'*80)

	matrix = complete_matrix(knapsack)
	melhor_valor = best_value(matrix)

	print('Mochila:')
	knapsack.showPrettyKnapsack()

	print('\nResultado = O melhor valor obtido é {} com os itens:'
	 	  .format(melhor_valor))

	i = len(matrix) - 1
	j = len(matrix[0]) - 1
	find(knapsack, matrix, i, j)
	
	print('-'*80)

k = Knapsack()
k.setMaxWeight(8)
k.setItems([1,2,3,4])
k.setValues([15,10,9,5])
k.setWeights([1,5,3,4])

run(k)

e = Knapsack()
e.setMaxWeight(11)
e.setItems([1,2,3,4,5])
e.setValues([1,6,18,22,28])
e.setWeights([1,2,5,6,7])

run(e)
