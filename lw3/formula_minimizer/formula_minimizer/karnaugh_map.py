from .minimizer_engine import *
from .minimizer_engine import _quine_mccluskey, _minimize_cover, _implicant_to_string


def optimize_kmap_dnf(table, verbose=True):
    kmap, variables = build_kmap(table)
    n_vars = len(variables)

    if kmap is None or n_vars == 0:
        return "0"

    if verbose:
        print_kmap(kmap, n_vars)

    rectangles = find_rectangles(kmap, n_vars, target=1)
    if not rectangles:
        return "0"

    terms = []
    for row, val in table:
        if val:
            t = tuple(row[v] for v in variables)
            terms.append(t)

    prime_implicants = _quine_mccluskey(terms, verbose)
    essential_implicants = _minimize_cover(prime_implicants, terms, verbose)

    dnf_terms = []
    for imp in essential_implicants:
        dnf_terms.append(_implicant_to_string(imp, variables, True))

    if not dnf_terms:
        return "0"
    return " | ".join(dnf_terms)


def optimize_kmap_cnf(table, verbose=True):
    kmap, variables = build_kmap(table)
    n_vars = len(variables)

    if kmap is None or n_vars == 0:
        return "1"

    if verbose:
        print_kmap(kmap, n_vars)

    # Поиск прямоугольников из нулей
    rectangles = find_rectangles(kmap, n_vars, target=0)
    if not rectangles:
        return "1"

    terms = []
    for row, val in table:
        if not val:
            t = tuple(row[v] for v in variables)
            terms.append(t)

    if not terms:
        return "1"

    prime_implicants = _quine_mccluskey(terms, verbose)
    essential_implicants = _minimize_cover(prime_implicants, terms, verbose)

    cnf_terms = []
    for imp in essential_implicants:
        cnf_terms.append(_implicant_to_string(imp, variables, False))

    if not cnf_terms:
        return "1"

    return " & ".join(cnf_terms)