import unittest

from logical_interpreter.logical_interpreter.log_ast import Var, And, Or, Not, Implies, Equiv

class TestLogicalOperations(unittest.TestCase):
    def test_variable_evaluation(self):
        env = {'a': True, 'b': False}
        self.assertTrue(Var('a').eval(env))
        self.assertFalse(Var('b').eval(env))

    def test_and_operation(self):
        env = {'a': True, 'b': False}
        self.assertFalse(And(Var('a'), Var('b')).eval(env))
        self.assertTrue(And(Var('a'), Var('a')).eval(env))

    def test_or_operation(self):
        env = {'a': True, 'b': False}
        self.assertTrue(Or(Var('a'), Var('b')).eval(env))
        self.assertFalse(Or(Var('b'), Var('b')).eval(env))

    def test_not_operation(self):
        env = {'a': True, 'b': False}
        self.assertFalse(Not(Var('a')).eval(env))
        self.assertTrue(Not(Var('b')).eval(env))

    def test_implies_operation(self):
        env = {'a': True, 'b': False}
        self.assertFalse(Implies(Var('a'), Var('b')).eval(env))
        self.assertTrue(Implies(Var('b'), Var('a')).eval(env))
        self.assertTrue(Implies(Var('b'), Var('b')).eval(env))

    def test_equiv_operation(self):
        env = {'a': True, 'b': False}
        self.assertFalse(Equiv(Var('a'), Var('b')).eval(env))
        self.assertTrue(Equiv(Var('a'), Var('a')).eval(env))
        self.assertTrue(Equiv(Var('b'), Var('b')).eval(env))

if __name__ == '__main__':
    unittest.main()