class GroupAction(object):
    """docstring for GroupAction"""
    def __init__(self, group, space, action = lambda g,x : x):
        self.group = group
        self.space = space
        self.action = action

    def act(self, group_element, element):
        return self.action(group_element, element)

class Group(object):
    def __init__(self, group_elements, operation):
        self.group_elements = set(group_elements)
        self.operation = operation

    def multiply(self, elem_1, elem_2):
        return self.operation(elem_1, elem_2)

#warning: does not terminate if semigroup generated by generators is not finite
def generate_finite_semigroup(generators, operation):
    elements = set()

    elements_to_add = set(generators)

    while elements_to_add:
        for element in elements_to_add:
            elements.add(element)

        recently_added_elements = elements_to_add
        elements_to_add = set()
        for generator in generators:
            for element in recently_added_elements:
                new_element = operation(generator, element)
                if new_element not in elements:
                    elements_to_add.add(new_element)

    return elements

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



if __name__ == '__main__':

    generators = set()
    generators.add((1,2,3,4,5,0))
    generators.add((1,0,5,4,3,2))
    
    dihedral_group_elements = generate_finite_semigroup(generators, multiply_permutations)
    dihedral_group = Group(dihedral_group_elements, multiply_permutations)

    action_on_pentagon = GroupAction(dihedral_group, set([0,1,2,3,4]), lambda g,x: g[x])

    print (len(dihedral_group_elements))

    print (calculate_setwise_stabilizer(action_on_pentagon, set([0,2,3])))

