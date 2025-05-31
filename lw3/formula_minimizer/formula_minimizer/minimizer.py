import logical_interpreter

from .calculative_method import calculated_method_dnf, calculated_method_cnf
from .tabular_method import tabular_method_dnf, tabular_method_cnf
from .karnaugh_map import optimize_kmap_dnf, optimize_kmap_cnf

class Formula(logical_interpreter.Formula):
    def __init__(self, formula: str) -> None:
        super().__init__(formula)
        self.min_terms = []
        self.max_terms = []
        for bits, value in self.truth_table:
            term_index = int("".join(map(str, list(bits.values()))), 2)
            self.min_terms.append(term_index) if value else self.max_terms.append(term_index)


    def calculated_method_dnf(self):
        return calculated_method_dnf(self.truth_table)

    def calculated_method_cnf(self):
        return calculated_method_cnf(self.truth_table)

    def tabular_method_dnf(self):
        return tabular_method_dnf(self.truth_table)

    def tabular_method_cnf(self):
        return tabular_method_cnf(self.truth_table)

    def kmap_method_dnf(self):
        return optimize_kmap_dnf(self.truth_table)

    def kmap_method_cnf(self):
        return optimize_kmap_cnf(self.truth_table)