import galois
import numpy as np

class PrimeOrderField(object):
	"""docstring for PrimeOrderFIeld"""
	def __init__(self, p):
		self.p = p
		self._GF = galois.GF(p)

	def matmul(self, matrix_1, matrix_2):
		product = np.matmul(self._GF(list(list(row) for row in matrix_1)), self._GF(list(list(row) for row in matrix_2)))

		return tuple([tuple([int(entry) for entry in row]) for row in product])

	def apply_lin_op(self, matrix, vector):
		return tuple(entry[0] for entry in self.matmul(matrix, [[entry] for entry in vector]))

	def generate_space(self, dim):
		if dim == 1:
			return set(tuple([x]) for x in range(self.p))

		dim_less_one = self.generate_space(dim - 1)
		space = set()

		for x in range(self.p):
			for vec in dim_less_one:
				space.add(tuple(list(vec) + [x]))

		return space

	def generate_matrices(self, dim, invertible_only = False):
		pass

if __name__ == '__main__':
	F2 = PrimeOrderField(2)

	print( F2.apply_lin_op(((1,1), (0,1)), (1,1) ) )

	print ("3D space", F2.generate_space(3))


