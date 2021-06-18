import time

class GroupAction(object):
    """docstring for GroupAction"""
    def __init__(self, group, space, action = lambda g,x : x):
        self.group = group
        self.space = space
        self.action = action

    def act(self, group_element, element):
        return self.action(group_element, element)

    def in_setwise_stabilizer(self, group_element, subset):
        return preserves_subset(lambda x: self.action(group_element, x), subset)

def preserves_subset(transformation, subset):
    for element in subset:
        if transformation(element) not in subset:
            return False

    return True

class Group(object):
    def __init__(self, group_elements, operation):
        self.group_elements = set(group_elements)
        self.operation = operation

    def multiply(self, elem_1, elem_2):
        return self.operation(elem_1, elem_2)

#warning: does not terminate if semigroup generated by generators is not finite
def generate_finite_semigroup(generators, operation, bad_element_callback = lambda x: False):
    elements = set()

    elements_to_add = set()

    for generator in generators:
        # want to bail early if we don't like this element
        if bad_element_callback(generator):
            return False

        elements_to_add.add(generator)

    while elements_to_add:
        for element in elements_to_add:
            elements.add(element)

        recently_added_elements = elements_to_add
        elements_to_add = set()
        for generator in generators:
            for element in recently_added_elements:
                new_element = operation(generator, element)
                if new_element not in elements:
                    # want to bail early if we don't like this element
                    if bad_element_callback(new_element):
                        return False
                    elements_to_add.add(new_element)

    return elements

# given two group operations, create the direct sum
def product_operation(op1, op2):
    return lambda pair_1, pair_2: (op1(pair_1[0], pair_2[0]), op2(pair_1[1], pair_2[1]))

# tests if there is an isomorphism mapping generators_1[i] to generators_2[i] for all i
# this is true if and only if the the subgroup generated by all tuples of the form (generators_1[i], generators_2[i]) in
# the direct product is the graph of an isomorphism (i.e., satisfies vertical and horizonal line tests)
# returns False if no such isomorphism exists and returns a tuple of maps otherwise, where each map is the isomorphism
def test_isomorphism(generators_1, generators_2, op_1, op_2):
    if len(generators_1) != len(generators_2):
        print ("generators not same length!")
        return False

    generators = [(generators_1[i], generators_2[i]) for i in range(len(generators_1))]

    x_to_y_map = {}
    y_to_x_map = {}
    product_subgroup = generate_finite_semigroup(generators, product_operation(op_1, op_2), 
        lambda candidate_tuple: line_test_helper(candidate_tuple, x_to_y_map, y_to_x_map))

    if product_subgroup == False:
        return False
    
    return (x_to_y_map, y_to_x_map)


def line_test_helper(candidate_tuple, x_to_y_map, y_to_x_map):
    if (candidate_tuple[0] in x_to_y_map) or (candidate_tuple[1] in y_to_x_map):
        return True

    x_to_y_map[candidate_tuple[0]] = candidate_tuple[1]
    y_to_x_map[candidate_tuple[1]] = candidate_tuple[0]

    return False


def multiply_permutations(perm_1, perm_2):
    result = []
    assert(len(perm_1) == len(perm_2))
    for value in perm_2:
        result.append(perm_1[value])

    return tuple(result)


def calculate_setwise_stabilizer(group_action, subset):
    stabilizer = set()
    for group_element in group_action.group.group_elements:
        in_stabilizer = True
        for element in subset:
            if group_action.act(group_element, element) not in subset:
                in_stabilizer = False
                break

        if in_stabilizer:
            stabilizer.add(group_element)

    return stabilizer

def generate_permutation_group(generator_set):
    group_elements = generate_finite_semigroup(generator_set, multiply_permutations)

    return Group(group_elements, multiply_permutations)

def generate_permutation_group_action(generator_set):
    acting_set = set(range(len(list(generator_set)[0])))

    return GroupAction(generate_permutation_group(generator_set), acting_set, lambda g,x: g[x])

#generate the symmetric group using the transpositions that swap adjacent elements
def generate_symmetric_group(n):
    generators = set()
    for i in range(n-1):
        swap_i = list(range(n))
        swap_i[i] = i+1
        swap_i[i+1] = i

        swap_i = tuple(swap_i)

        generators.add(swap_i)

    return generate_permutation_group(generators)

def is_identity_perm(perm):
    return ( perm == tuple(range(len(perm))) )

def perm_group_is_transitive(group_elements):
    space = None
    for group_element in group_elements:
        if space is None:
            space = set(range(len(group_element)))

        if group_element[0] in space:
            space.remove(group_element[0])

        if not space:
            return True

    return False

def construct_k_distinct_tuples(input_list, k):
    if k == 1:
        return [tuple([x]) for x in input_list]

    k_minus_one_tuples = construct_k_distinct_tuples(input_list, k -1)

    result = []
    for tuple_ in k_minus_one_tuples:
        for x in input_list:
            if x not in tuple_:
                result.append(tuple(list(tuple_) + [x]))

    return result


class ConjectureTester(object):
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


def test_transitivity_tester():
    generators = set()

    generators.add((1,0,2,3,4))
    generators.add((2,0,1,4,3))

    assert( False == perm_group_is_transitive(generate_finite_semigroup(generators, multiply_permutations)) )

    generators = set()

    generators.add((1,2,3,0))

    assert( True == perm_group_is_transitive(generate_finite_semigroup(generators, multiply_permutations)) )


if __name__ == '__main__':

    generators = set()
    generators.add((1,2,3,4,5,0))
    generators.add((1,0,5,4,3,2))
    
    action_on_pentagon = generate_permutation_group_action(generators)

    print (len(action_on_pentagon.group.group_elements))

    print (calculate_setwise_stabilizer(action_on_pentagon, set([0,2,3])))

    result = test_isomorphism([(1,2,3,0)], [(3,0,1,2)], multiply_permutations, multiply_permutations)

    for x in result[0]:
        print (x, result[0][x])

    print("testing transitivity...")

    test_transitivity_tester()
    
    n = 3
    while True:
        print ("testing n = ", n)
        for i in range(3,n):
            print ("testing subset size = ", i)
            ConjectureTester().test_conjecture(n, 2, test_subset_size = i)
        n += 1