import unittest

from formula_minimizer.formula_minimizer.minimizer import Formula

class TestCalculativeMethod(unittest.TestCase):
    def test_calculative_method(self):
        formula = Formula('!A|B&C')
        self.assertEqual(formula.calculated_method_cnf(), '(!A | B) & (!A | C)')
        self.assertEqual(formula.calculated_method_dnf(), '(!A) | (B & C)')

        formula = Formula('(!A)&(B|C)')
        self.assertEqual(formula.calculated_method_cnf(), '(!A) & (B | C)')
        self.assertEqual(formula.calculated_method_dnf(), '(!A & C) | (!A & B)')

        formula = Formula('(A->B)&(!C)&(D|E)')
        self.assertEqual(formula.calculated_method_cnf(), '(!C) & (D | E) & (!A | B)')
        self.assertEqual(formula.calculated_method_dnf(), '(!A & !C & E) | (B & !C & D) | (!A & !C & D) | (B & !C & E)')


class TestTabularMethod(unittest.TestCase):
    def test_tabular_method(self):
        formula = Formula('!A|B&C')
        self.assertEqual(formula.tabular_method_cnf(), '(!A | B) & (!A | C)')
        self.assertEqual(formula.tabular_method_dnf(), '(!A) | (B & C)')

        formula = Formula('!A&(B|C)')
        self.assertEqual(formula.tabular_method_cnf(), '(!A) & (B | C)')
        self.assertEqual(formula.tabular_method_dnf(), '(!A & C) | (!A & B)')

        formula = Formula('(A->B)&(!C)&(D|E)')
        self.assertEqual(formula.tabular_method_cnf(), '(!C) & (D | E) & (!A | B)')
        self.assertEqual(formula.tabular_method_dnf(), '(!A & !C & E) | (B & !C & D) | (!A & !C & D) | (B & !C & E)')


class TestKmap(unittest.TestCase):
    def test_calculative_method(self):
        formula = Formula('!A|B&C')
        self.assertEqual(formula.kmap_method_cnf(), '(!A | B) & (!A | C)')
        self.assertEqual(formula.kmap_method_dnf(), '(!A) | (B & C)')

        formula = Formula('!A&(B|C)')
        self.assertEqual(formula.kmap_method_cnf(), '(!A) & (B | C)')
        self.assertEqual(formula.kmap_method_dnf(), '(!A & C) | (!A & B)')

        formula = Formula('(A->B)&(!C)&(D|E)')
        self.assertEqual(formula.kmap_method_cnf(), '(!C) & (D | E) & (!A | B)')
        self.assertEqual(formula.kmap_method_dnf(), '(!A & !C & E) | (B & !C & D) | (!A & !C & D) | (B & !C & E)')


if __name__ == '__main__':
    unittest.main()