from group_theory import *

def test_transitivity_tester():
    generators = set()

    generators.add((1,0,2,3,4))
    generators.add((2,0,1,4,3))

    assert( False == perm_group_is_transitive(generate_finite_semigroup(generators, multiply_permutations)) )

    generators = set()

    generators.add((1,2,3,0))

    assert( True == perm_group_is_transitive(generate_finite_semigroup(generators, multiply_permutations)) )

def test_dihedral():
    generators = set()
    generators.add((1,2,3,4,5,0))
    generators.add((1,0,5,4,3,2))
    
    action_on_pentagon = generate_permutation_group_action(generators)

    assert( 12 == len(action_on_pentagon.group.group_elements))

def test_isomorphism_tester():
    result = test_isomorphism([(1,2,3,0)], [(3,0,1,2)], multiply_permutations, multiply_permutations)
    assert ( result != False)

if __name__ == '__main__':
    test_transitivity_tester()
    test_dihedral()
    test_isomorphism_tester()
