import galois
import numpy as np

from group_theory import *

class PrimeOrderField(object):
    """wrapper for the galois library, enables linear algebra in field with prime power number of elements"""
    def __init__(self, p):
        self.p = p
        self._GF = galois.GF(p)

    def matmul(self, matrix_1, matrix_2):
        product = np.matmul(self._GF(list(list(row) for row in matrix_1)), self._GF(list(list(row) for row in matrix_2)))

        return tuple([tuple([int(entry) for entry in row]) for row in product])

    def matinv(self, matrix):
        inverse = np.linalg.inv(self._GF(list(list(row) for row in matrix)))

        return tuple([tuple([int(entry) for entry in row]) for row in inverse])

    def transpose(self, matrix):
        trans = np.transpose(self._GF(list(list(row) for row in matrix)))

        return tuple([tuple([int(entry) for entry in row]) for row in trans])

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

    def generate_special_linear(self, dim):
        #TODO: more efficient, brute force it for now
        vectors = self.generate_space(dim)
        matrices = construct_k_distinct_tuples(vectors, dim)

        special_linear_matrices = set()

        for matrix in matrices:
            if (np.linalg.det(self._GF(matrix)) == 1):
                special_linear_matrices.add(matrix)

        return special_linear_matrices

class FanoPermData(object):
    """docstring for FanoPermData"""
    def __init__(self, g_perm, g_dual_perm):
        self.g_perm = g_perm
        self.g_dual_perm = g_dual_perm

def create_vector_id_maps(vectors):
    id_to_vector = dict()
    vector_to_id = dict()

    vector_id = 0
    for vector in vectors:
        id_to_vector[vector_id] = vector
        vector_to_id[vector] = vector_id

        vector_id += 1

    return (id_to_vector, vector_to_id)

def convert_linear_group_to_permutation(base_field, vectors, group):
    id_to_vector, vector_to_id = create_vector_id_maps(vectors)      

    g_perm_list = []
    g_dual_perm_list = []
    for matrix in group:
        g_perm = []
        g_tran_inv_perm = []
        for vec_id in id_to_vector:
            g_perm.append(vector_to_id[base_field.apply_lin_op(matrix, id_to_vector[vec_id])])
            g_tran_inv_perm.append(vector_to_id[base_field.apply_lin_op(base_field.transpose(base_field.matinv(matrix)), id_to_vector[vec_id])])

        g_perm_list.append(tuple(g_perm))
        g_dual_perm_list.append(tuple(g_tran_inv_perm))

    return FanoPermData(g_perm_list, g_dual_perm_list)

def create_fano_plane_permutations():
    F2 = PrimeOrderField(2)

    vectors = F2.generate_space(3)
    vectors.remove((0,0,0))

    sl_3 = F2.generate_special_linear(3)

    return convert_linear_group_to_permutation(F2, vectors, sl_3)

def create_fano_21_Frob():
    F8 = galois.GF(8)

    tau = tuple(int(F8(x) * F8(3)) - 1 for x in range(1,8))
    sigma = tuple(int(F8(x) * F8(x)) - 1 for x in range(1,8))

    tau = lambda x: int(F8(x) * F8(3))
    sigma = lambda x: int(F8(x) * F8(x))

    F2 = PrimeOrderField(2)

    tau = int_map_to_matrix(tau)
    sigma = int_map_to_matrix(sigma)

    group = generate_finite_semigroup([tau, sigma], lambda A,B: F2.matmul(A,B))

    vectors = F2.generate_space(3)
    vectors.remove((0,0,0))

    return convert_linear_group_to_permutation(F2, vectors, group)


def F8vector_to_int(vector):
    return int(''.join([str(bit) for bit in vector]), 2)

def int_to_F8vector(int_rep):
    return(tuple(int(bit) for bit in '{0:03b}'.format(int_rep)))

#convert a map in F8 to the matrix representation in (F_2)^3
def int_map_to_matrix(int_map):
    basis = [(1,0,0), (0,1,0), (0,0,1)]

    matrix_transpose = ([int_to_F8vector(int_map(F8vector_to_int(basis_vector))) for basis_vector in basis])
    F2 = PrimeOrderField(2)

    return F2.transpose(matrix_transpose)

if __name__ == '__main__':
    F2 = PrimeOrderField(2)

    #print( F2.apply_lin_op(((1,1), (0,1)), (1,1) ) )

    #print ("3D space", F2.generate_space(3))

    #print( len(F2.generate_special_linear(3)))

    #print ("inverse of [0,1; 1 0] is", F2.matinv( ((0,1),(1,0))) )

    fano_perm_data = create_fano_plane_permutations()

    print (len(fano_perm_data.g_dual_perm))

    print(len(create_fano_21_Frob().g_dual_perm))


