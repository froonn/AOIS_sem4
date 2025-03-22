from logical_interpreter.logical_interpreter.log_parser import parse

class Table:
    def __init__(self, logical_formula: str) -> None:
        self.func = parse(logical_formula)
        self.variables = self.func.vars
        self.truth_table = self.generate_truth_table()

    def generate_truth_table(self) -> list[tuple[dict[str, int], bool]]:
        from itertools import product
        table = []
        for values in product([0, 1], repeat=len(self.variables)):
            env = dict(zip(self.variables, values))
            result = self.func(env)
            table.append((env, result))
        return table

    def print_truth_table(self) -> None:
        header = self.variables + ['Result']
        print(' | '.join(header))
        print('-' * (len(header) * 4 - 1))
        for row in self.truth_table:
            values = [str(row[0][var]) for var in self.variables] + [str(int(row[1]))]
            print(' | '.join(values))

    def disjunctive_form(self) -> str:
        terms = []
        for env, result in self.truth_table:
            if result:
                term = ' & '.join(f'{var}' if val else f'!{var}' for var, val in env.items())
                terms.append(f'({term})')
        return ' | '.join(terms)

    def disjunction_digital_form(self) -> str:
        indices = [str(i) for i, (_, result) in enumerate(self.truth_table) if result]
        return f'| ({", ".join(indices)})'

    def conjunctive_form(self) -> str:
        terms = []
        for env, result in self.truth_table:
            if not result:
                term = ' | '.join(f'{var}' if not val else f'!{var}' for var, val in env.items())
                terms.append(f'({term})')
        return ' & '.join(terms)

    def conjunction_digital_form(self) -> str:
        indices = [str(i) for i, (_, result) in enumerate(self.truth_table) if not result]
        return f'& ({", ".join(indices)})'

    def index_form(self) -> str:
        binary_form = ''.join(str(int(result)) for _, result in self.truth_table)
        decimal_form = str(int(binary_form, 2))
        return f'Binary: {binary_form}, Decimal: {decimal_form}'