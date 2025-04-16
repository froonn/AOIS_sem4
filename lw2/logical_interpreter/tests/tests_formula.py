import io
import unittest
import unittest.mock

from logical_interpreter.logical_interpreter.log_formula import Formula

class TestFormula(unittest.TestCase):
    def test_generates_correct_truth_table(self):
        table = Formula("a & b")
        expected_truth_table = [
            ({'a': 0, 'b': 0}, False),
            ({'a': 0, 'b': 1}, False),
            ({'a': 1, 'b': 0}, False),
            ({'a': 1, 'b': 1}, True)
        ]
        self.assertEqual(table.truth_table, expected_truth_table)

    def test_prints_correct_truth_table(self):
        table = Formula("a & b")
        expected_output = "a | b | Result\n-----------\n0 | 0 | 0\n0 | 1 | 0\n1 | 0 | 0\n1 | 1 | 1\n"
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            table.print_truth_table()
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_generates_disjunctive_form(self):
        table = Formula("a & b")
        self.assertEqual(table.disjunctive_form(), "(a & b)")

    def test_generates_disjunction_digital_form(self):
        table = Formula("a & b")
        self.assertEqual(table.disjunction_digital_form(), "| (3)")

    def test_generates_conjunctive_form(self):
        table = Formula("a & b")
        self.assertEqual(table.conjunctive_form(), "(a | b) & (a | !b) & (!a | b)")

    def test_generates_conjunction_digital_form(self):
        table = Formula("a & b")
        self.assertEqual(table.conjunction_digital_form(), "& (0, 1, 2)")

    def test_generates_index_form(self):
        table = Formula("a & b")
        self.assertEqual(table.index_form(), "Binary: 0001, Decimal: 1")

if __name__ == '__main__':
    unittest.main()