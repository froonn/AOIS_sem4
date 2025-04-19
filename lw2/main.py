from logical_interpreter import Formula

"""
!(A->(!B|B&C)~(D&!(C->B)))
"""

while True:
    formula = input('Enter logical formula (or exit): ')

    if formula == 'exit':
        break

    formula = Formula(formula)
    
    print('Table')
    formula.print_truth_table()

    print('Disjunctive Form:', formula.disjunctive_form())
    print('Disjunction Digital Form:', formula.disjunction_digital_form())
    print('Conjunctive Form:', formula.conjunctive_form())
    print('Conjunction Digital Form:', formula.conjunction_digital_form())
    print('Index Form:', formula.index_form())
    print()