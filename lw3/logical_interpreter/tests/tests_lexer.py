import unittest
import re

from logical_interpreter.logical_interpreter.lexer import lex

class TestLexer(unittest.TestCase):
    def setUp(self):
        self.token_patterns = [
            (re.compile(r'\s+'), None),  # Whitespace
            (re.compile(r'\('), 'LPAREN'),
            (re.compile(r'\)'), 'RPAREN'),
            (re.compile(r'~'), 'NOT'),
            (re.compile(r'&'), 'AND'),
            (re.compile(r'\|'), 'OR'),
            (re.compile(r'->'), 'IMPLIES'),
            (re.compile(r'<->'), 'EQUIV'),
            (re.compile(r'[a-zA-Z_]\w*'), 'VAR')
        ]

    def test_valid_input(self):
        characters = "(a & b) | ~c"
        expected_tokens = [('(', 'LPAREN'), ('a', 'VAR'), ('&', 'AND'), ('b', 'VAR'), (')', 'RPAREN'), ('|', 'OR'), ('~', 'NOT'), ('c', 'VAR')]
        self.assertEqual(lex(characters, self.token_patterns), expected_tokens)

    def test_invalid_character(self):
        characters = "(a & b) | ~c$"
        with self.assertRaises(SyntaxError):
            lex(characters, self.token_patterns)

    def test_empty_input(self):
        characters = ""
        expected_tokens = []
        self.assertEqual(lex(characters, self.token_patterns), expected_tokens)

    def test_only_whitespace(self):
        characters = "   \t\n"
        expected_tokens = []
        self.assertEqual(lex(characters, self.token_patterns), expected_tokens)

    def test_complex_expression(self):
        characters = "(a <-> b) & ~(c -> d)"
        expected_tokens = [('(', 'LPAREN'), ('a', 'VAR'), ('<->', 'EQUIV'), ('b', 'VAR'), (')', 'RPAREN'), ('&', 'AND'), ('~', 'NOT'), ('(', 'LPAREN'), ('c', 'VAR'), ('->', 'IMPLIES'), ('d', 'VAR'), (')', 'RPAREN')]
        self.assertEqual(lex(characters, self.token_patterns), expected_tokens)

if __name__ == '__main__':
    unittest.main()