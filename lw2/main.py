from logical_interpreter import Table

"""
!(s->(!r|r&q)~(p&!(q->r)))
"""

while True:


    formula = input('Enter logical formula: ')

    table = Table(formula)
    
    print('Table')
    table.print_truth_table()

    print('Disjunctive Form:', table.disjunctive_form())
    print('Disjunction Digital Form:', table.disjunction_digital_form())
    print('Conjunctive Form:', table.conjunctive_form())
    print('Conjunction Digital Form:', table.conjunction_digital_form())
    print('Index Form:', table.index_form())
    print()