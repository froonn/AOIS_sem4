import unittest

from formula_minimizer.formula_minimizer.minimizer import Formula

class TestCalculativeMethod(unittest.TestCase):
    def test_calculative_method(self):
        formula = Formula('!A|B&C')
        self.assertEqual(formula.calculated_method_cnf(), '(A|!C) & (A|!B)')
        self.assertEqual(formula.calculated_method_dnf(), '(!B&!C) | (A)')

        formula = Formula('(!A)&(B|C)')

        self.assertEqual(formula.calculated_method_cnf(), '(!B|!C) & (A)')
        self.assertEqual(formula.calculated_method_dnf(), '(A&!C) | (A&!B)')


class TestTabularMethod(unittest.TestCase):
    def test_tabular_method(self):
        formula = Formula('!A|B&C')
        self.assertEqual(formula.tabular_method_cnf(), '(A|!C) & (A|!B)')
        self.assertEqual(formula.tabular_method_dnf(), '(!B&!C) | (A)')

        formula = Formula('!A&(B|C)')
        self.assertEqual(formula.tabular_method_cnf(), '(!B|!C) & (A)')
        self.assertEqual(formula.tabular_method_dnf(), '(A&!C) | (A&!B)')


class TestKmap(unittest.TestCase):
    def test_calculative_method(self):
        formula = Formula('!A|B&C')
        self.assertEqual(' | '.join(formula.kmap_method_dnf()), '(!A&B&!C) | (!A&!B&!C) | (!A&!B&C) | (A&B&C) | (!A&B&C)')
        self.assertEqual(' & '.join(formula.kmap_method_cnf()), '(!A|B|C) & (!A|B|!C) & (!A|!B|C)')

        formula = Formula('!A&(B|C)')
        self.assertEqual(' & '.join(formula.kmap_method_cnf()), '(!A|B|!C) & (!A|!B|C) & (A|B|C) & (!A|B|C) & (!A|!B|!C)')
        self.assertEqual(' | '.join(formula.kmap_method_dnf()), '(!A&!B&C) | (!A&B&!C) | (!A&B&C)')


if __name__ == '__main__':
    unittest.main()