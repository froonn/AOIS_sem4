class Expr:
    """
    Base class for all expressions in the logical formula.
    """
    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluate the expression in the given environment.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The result of evaluating the expression.
        """
        pass

class Var(Expr):
    """
    Class representing a variable in the logical formula.
    """
    def __init__(self, name: str) -> None:
        """
        Initialize a variable with the given name.

        Args:
            name (str): The name of the variable.
        """
        self.name = name

    def __repr__(self) -> str:
        """
        Return a string representation of the variable.

        Returns:
            str: The string representation of the variable.
        """
        return f'Var({self.name})'

    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluate the variable in the given environment.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The value of the variable in the given environment.
        """
        return env[self.name]

class And(Expr):
    """
    Class representing a logical AND operation.
    """
    def __init__(self, left: Var, right: Var) -> None:
        """
        Initialize an AND operation with the given left and right operands.

        Args:
            left (Var): The left operand.
            right (Var): The right operand.
        """
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        """
        Return a string representation of the AND operation.

        Returns:
            str: The string representation of the AND operation.
        """
        return f'And({self.left}, {self.right})'

    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluate the AND operation in the given environment.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The result of the AND operation.
        """
        return self.left.eval(env) and self.right.eval(env)

class Or(Expr):
    """
    Class representing a logical OR operation.
    """
    def __init__(self, left: Var, right: Var) -> None:
        """
        Initialize an OR operation with the given left and right operands.

        Args:
            left (Var): The left operand.
            right (Var): The right operand.
        """
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        """
        Return a string representation of the OR operation.

        Returns:
            str: The string representation of the OR operation.
        """
        return f'Or({self.left}, {self.right})'

    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluate the OR operation in the given environment.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The result of the OR operation.
        """
        return self.left.eval(env) or self.right.eval(env)

class Not(Expr):
    """
    Class representing a logical NOT operation.
    """
    def __init__(self, operand: Var) -> None:
        """
        Initialize a NOT operation with the given operand.

        Args:
            operand (Var): The operand.
        """
        self.operand = operand

    def __repr__(self) -> str:
        """
        Return a string representation of the NOT operation.

        Returns:
            str: The string representation of the NOT operation.
        """
        return f'Not({self.operand})'

    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluate the NOT operation in the given environment.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The result of the NOT operation.
        """
        return not self.operand.eval(env)

class Implies(Expr):
    """
    Class representing a logical implication operation.
    """
    def __init__(self, left: Var, right: Var) -> None:
        """
        Initialize an implication operation with the given left and right operands.

        Args:
            left (Var): The left operand.
            right (Var): The right operand.
        """
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        """
        Return a string representation of the implication operation.

        Returns:
            str: The string representation of the implication operation.
        """
        return f'Implies({self.left}, {self.right})'

    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluate the implication operation in the given environment.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The result of the implication operation.
        """
        return not self.left.eval(env) or self.right.eval(env)

class Equiv(Expr):
    """
    Class representing a logical equivalence operation.
    """
    def __init__(self, left: Var, right: Var) -> None:
        """
        Initialize an equivalence operation with the given left and right operands.

        Args:
            left (Var): The left operand.
            right (Var): The right operand.
        """
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        """
        Return a string representation of the equivalence operation.

        Returns:
            str: The string representation of the equivalence operation.
        """
        return f'Equiv({self.left}, {self.right})'

    def eval(self, env: dict[str, bool]) -> bool:
        """
        Evaluate the equivalence operation in the given environment.

        Args:
            env (dict[str, bool]): A dictionary mapping variable names to their boolean values.

        Returns:
            bool: The result of the equivalence operation.
        """
        return self.left.eval(env) == self.right.eval(env)