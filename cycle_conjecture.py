from group_theory import *

class CycleConjectureTester(object):
    def __init__(self,n):
        self.s_n = generate_symmetric_group(n).group_elements

    def test_conjecture_generators(self, gen_tuple_1, gen_tuple_2):
        if not self.check_conjugate(gen_tuple_1, gen_tuple_2):
            if self.check_fixed_points_equal(gen_tuple_1, gen_tuple_2):
                print ("found counterexample!", gen_tuple_1, gen_tuple_2)

    def test_conjecture_all_tuples(self, k):
        generator_tuples = construct_k_distinct_tuples(list(self.s_n), k)

        for gen_tuple_1 in generator_tuples:
            for gen_tuple_2 in generator_tuples:
                self.test_conjecture_generators(gen_tuple_1, gen_tuple_2)

        print ("found no counterexample on ", k, "generators")

    def check_fixed_points_equal(self, generators_1, generators_2):
        generators = [(generators_1[i], generators_2[i]) for i in range(len(generators_1))]

        product_subgroup = generate_finite_semigroup(
            generators, 
            product_operation(multiply_permutations, multiply_permutations), 
            lambda perm_pair : ( count_fixed_points(perm_pair[0]) != count_fixed_points(perm_pair[1]) )
            )

        return (product_subgroup is not False)

    def check_conjugate(self, generators_1, generators_2):
        conjugator_candidates = self.s_n
        for i in range(len(generators_1)):
            conjugator_candidates = get_perm_conjugators(generators_1[i], generators_2[i], conjugator_candidates)
            if len(conjugator_candidates) == 0:
                return False

        return (len(conjugator_candidates) > 0)

if __name__ == '__main__':
    CycleConjectureTester(5).test_conjecture_all_tuples(2)



