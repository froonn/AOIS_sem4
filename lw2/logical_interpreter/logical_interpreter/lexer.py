import re
from typing import List, Tuple

def lex(characters: str, token_patterns: List[Tuple[re.Pattern, str]]) -> List[Tuple[str, str]]:
    """
    Lexical analyzer that tokenizes a string based on given token patterns.

    Args:
        characters (str): The input string to be tokenized.
        token_patterns (List[Tuple[re.Pattern, str]]): A list of tuples where each tuple contains a regex pattern (re.Pattern) and a tag (str).

    Returns:
        List[Tuple[str, str]]: A list of tokens where each token is a tuple containing the matched text and its corresponding tag.

    Raises:
        ValueError: If an illegal character is encountered in the input string.
    """
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for regex, tag in token_patterns:
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            raise SyntaxError('Illegal character: %s\n' % characters[pos])
        pos = match.end(0)
    return tokens
