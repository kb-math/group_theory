from group_theory import *

class ReturnTimesConjectureTester(object):
    """docstring for ConjectureTester"""
    def __init__(self):
        self.test_subset = set([0,1,2])
        self.candidate_actions = set()

    def preserves_subset(self, g):
        return preserves_subset(lambda x: g[x], self.test_subset)

    def test_subgroup_stabilizer(self, generator_list):
        test_setwise_stabilizer = lambda g: ((not is_identity_perm(g)) and self.preserves_subset(g)) 
        group_elements = generate_finite_semigroup(set(generator_list), multiply_permutations, test_setwise_stabilizer)

        if not group_elements:
            return False

        return group_elements

    def check_if_isomorphic_to_existing_subgroup(self, generator_tuple):
        group_is_new = True
        new_actions = set()
        for prev_generator_tuple in self.candidate_actions:
            result = test_isomorphism(list(generator_tuple), list(prev_generator_tuple), multiply_permutations, multiply_permutations)
            if result is not False:
                #we have found an isomorphic copy of a previous group, check if its action is isomorphic
                group_is_new = False
                are_isomorphic = self.check_if_action_isomorphic(result)
                if not are_isomorphic:
                    new_actions.add(generator_tuple)
                    #now check if their return times are the same
                    if self.check_return_times(result):
                        print("these two generators are counterexample:", generator_tuple, prev_generator_tuple)

        if group_is_new:
            new_actions.add(generator_tuple)

        self.candidate_actions.update(new_actions)

    def check_return_times(self, result):
        group_iso_dict = result[0]

        for group_element in group_iso_dict:
            if ((group_element[0] in self.test_subset) != (group_iso_dict[group_element][0] in self.test_subset)):
                return False

        print("return times agree!!!!!")
        return True


    def check_if_action_isomorphic(self, result):
        group_iso_dict = result[0]

        for group_element in group_iso_dict:
            #the two actions are isomorphic 
            # checking the stabilizer of 0 is enough
            if (group_element[0] == 0) != (group_iso_dict[group_element][0] == 0):
                return False

        return True

    def test_conjecture(self, n, r, test_subset_size = 2):
        self.test_subset = set(range(test_subset_size))
        symmetric_group = generate_symmetric_group(n)

        generator_tuple_list = construct_k_distinct_tuples(symmetric_group.group_elements, r)

        for generator_tuple in generator_tuple_list:
            result = self.test_subgroup_stabilizer(list(generator_tuple))
            if result == False:
                continue

            if not perm_group_is_transitive(result):
                continue

            group_elements = result

            self.check_if_isomorphic_to_existing_subgroup(generator_tuple)

def TestReturnTimesConjecture():
    n = 3
    while True:
        print ("testing n = ", n)
        for i in range(3,n):
            print ("testing subset size = ", i)
            ReturnTimesConjectureTester().test_conjecture(n, 2, test_subset_size = i)
        n += 1

if __name__ == '__main__':
    TestReturnTimesConjecture()

