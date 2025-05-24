from typing import Optional

from logical_interpreter.logical_interpreter.log_ast import *
from logical_interpreter.logical_interpreter.log_lexer import log_lex


class LogicalFormula:
    """
    Class representing a logical formula.

    Attributes:
        ast (Expr): The abstract syntax tree of the logical formula.
        vars (list[str]): The list of variables in the logical formula.
    """

    def __init__(self, ast: Expr, variables: list[str]) -> None:
        """
        Initializes a LogicalFormula instance.

        Args:
            ast (Expr): The abstract syntax tree of the logical formula.
            variables (list[str]): The list of variables in the logical formula.
        """
        self.ast = ast
        self.vars = variables

    def __call__(self, kwargs: dict[str, bool]) -> bool:
        """
        Evaluates the logical formula with the given variable assignments.

        Args:
            kwargs (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The result of evaluating the logical formula.
        """
        return self.ast.eval(kwargs)

def parse(logical_formula: str) -> LogicalFormula:
    """
    Parses a logical formula string into a LogicalFormula object.

    Args:
        logical_formula (str): The logical formula as a string.

    Returns:
        LogicalFormula: The parsed logical formula.
    """
    tokens = log_lex(logical_formula)
    parser = Parser(tokens)
    ast = parser.parse()

    variables = []
    for token in tokens:
        if token[1] == 'VAR' and token[0] not in variables:
            variables.append(token[0])

    return LogicalFormula(ast, variables)

class Parser:
    """
    Class for parsing tokens into an abstract syntax tree (AST) representing a logical formula.

    Attributes:
        tokens (list[tuple[str, str]]): The list of tokens to parse.
        pos (int): The current position in the token list.
    """

    def __init__(self, tokens: list[tuple[str, str]]) -> None:
        """
        Initializes a Parser instance.

        Args:
            tokens (list[tuple[str, str]]): The list of tokens to parse.
        """
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> Var:
        """
        Parses the tokens into an AST.

        Returns:
            Var: The root of the AST.

        Raises:
            SyntaxError: If there are unmatched parentheses.
        """
        result = self.expr()
        if self.pos < len(self.tokens):
            raise SyntaxError('Unexpected token after parsing complete')
        return result

    def match(self, expected_tag: str) -> Optional[str]:
        """
        Matches the current token with the expected tag and advances the position.

        Args:
            expected_tag (str): The expected token tag.

        Returns:
            Optional[str]: The matched token value, or None if no match.
        """
        if self.pos < len(self.tokens) and self.tokens[self.pos][1] == expected_tag:
            self.pos += 1
            return self.tokens[self.pos - 1][0]
        return None

    def expr(self) -> Var:
        """
        Parses an expression.

        Returns:
            Var: The parsed expression.
        """
        return self.equiv()

    def equiv(self) -> Var:
        """
        Parses an equivalence expression.

        Returns:
            Var: The parsed equivalence expression.
        """
        left = self.implies()
        while self.match('EQUIV'):
            right = self.implies()
            left = Equiv(left, right)
        return left

    def implies(self) -> Var:
        """
        Parses an implication expression.

        Returns:
            Var: The parsed implication expression.
        """
        left = self.or_expr()
        while self.match('IMPLIES'):
            right = self.or_expr()
            left = Implies(left, right)
        return left

    def or_expr(self) -> Var:
        """
        Parses an OR expression.

        Returns:
            Var: The parsed OR expression.
        """
        left = self.and_expr()
        while self.match('OR'):
            right = self.and_expr()
            left = Or(left, right)
        return left

    def and_expr(self) -> Var:
        """
        Parses an AND expression.

        Returns:
            Var: The parsed AND expression.
        """
        left = self.not_expr()
        while self.match('AND'):
            right = self.not_expr()
            left = And(left, right)
        return left

    def not_expr(self) -> Not | Var:
        """
        Parses a NOT expression.

        Returns:
            Not | Var: The parsed NOT expression or variable.
        """
        if self.match('NOT'):
            operand = self.not_expr()
            return Not(operand)
        return self.atom()

    def atom(self) -> Var:
        """
        Parses an atomic expression (variable or parenthesized expression).

        Returns:
            Var: The parsed atomic expression.

        Raises:
            SyntaxError: If an expected variable or parenthesis is not found.
        """
        if self.match('LPAREN'):
            expr = self.expr()
            if not self.match('RPAREN'):
                raise SyntaxError('Expected closing parenthesis')
            return expr
        var = self.match('VAR')
        if var:
            return Var(var)
        raise SyntaxError('Expected variable or parenthesis')