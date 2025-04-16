from logical_interpreter import Formula

"""
!(s->(!r|r&q)~(p&!(q->r)))
"""

while True:
    formula = input('Enter logical formula: ')

    formula = Formula(formula)
    
    print('Table')
    formula.print_truth_table()

    print('Disjunctive Form:', formula.disjunctive_form())
    print('Disjunction Digital Form:', formula.disjunction_digital_form())
    print('Conjunctive Form:', formula.conjunctive_form())
    print('Conjunction Digital Form:', formula.conjunction_digital_form())
    print('Index Form:', formula.index_form())
    print()