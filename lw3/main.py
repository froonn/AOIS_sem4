from formula_minimizer import Formula

"""
(A->B)&(!C)&(D|E)
!(A->(!B|B&C)~(D&!(C->B)))
"""


while True:
    formula = input('Enter logical formula: ')

    formula = Formula(formula)

    print('\n-- Таблица истинности --')
    formula.print_truth_table()

    print('\nСовершенная конъюнктивная нормальная форма:', formula.conjunctive_form())
    print('Цифровая форма:', formula.conjunction_digital_form())

    print('\nСовершенная дизъюнктивная нормальная форма:', formula.disjunctive_form())
    print('Цифровая форма:', formula.disjunction_digital_form())

    print('\nИндексная форма:', formula.index_form())

    print(formula.truth_table)

    dnf_calculated = formula.calculated_method_dnf()
    dnf_tabular = formula.tabular_method_dnf()
    dnf_kmap = formula.kmap_method_dnf()

    cnf_calculated = formula.calculated_method_cnf()
    cnf_tabular = formula.tabular_method_cnf()
    cnf_kmap = formula.kmap_method_cnf()

    print("\n-- Итоговый результат --")
    print("\nРезультаты минимизации для СДНФ:")
    print(f"  1) Расчетный метод: {dnf_calculated}")
    print(f"  2) Расчетно-табличный метод: {dnf_tabular}")
    print(f"  3) Метод Карно: {dnf_kmap}")

    print("\nРезультаты минимизации для СКНФ:")
    print(f"  1) Расчетный метод: {cnf_calculated}")
    print(f"  2) Расчетно-табличный метод: {cnf_tabular}")
    print(f"  3) Метод Карно: {cnf_kmap}")

    print()