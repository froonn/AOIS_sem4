import re
from typing import List, Tuple
from logical_interpreter.logical_interpreter import lexer

# Compile all regex patterns before the loop for efficiency
token_patterns: List[Tuple[re.Pattern, str]] = [(re.compile(pattern), tag) for pattern, tag in [
    (r'\s+',          None),  # Пробелы
    (r'\&',           'AND'),
    (r'\|',           'OR'),
    (r'\!',           'NOT'),
    (r'\->',          'IMPLIES'),
    (r'\~',           'EQUIV'),
    (r'\(',           'LPAREN'),
    (r'\)',           'RPAREN'),
    (r'[a-zA-Z_]\w*', 'VAR')
]]


def log_lex(characters: str) -> List[Tuple[str, str]]:
    """
    Lexical analyzer that tokenizes a string based on predefined token patterns.

    Args:
        characters (str): The input string to be tokenized.

    Returns:
        list of tuples: A list of tokens where each token is a tuple containing the matched text and its corresponding tag.
    """
    return lexer.lex(characters, token_patterns)
