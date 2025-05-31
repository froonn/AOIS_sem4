from .minimizer_engine import _get_binary_representation, _quine_mccluskey, _minimize_cover, _implicant_to_string

def calculated_method_dnf(table, verbose=True):
    if not table:
        return "0"
    variables = sorted(table[0][0].keys())
    terms = []
    for row, val in table:
        if val:
            t = _get_binary_representation(row, variables)
            terms.append(t)

    if not terms:
        return "0"

    prime_implicants = _quine_mccluskey(terms, verbose)
    essential_implicants = _minimize_cover(prime_implicants, terms, verbose)

    if not essential_implicants:
        return "0"

    for imp in essential_implicants:
        if all(x is None for x in imp):
            return "1"

    dnf_terms = []
    for imp in essential_implicants:
        dnf_terms.append(_implicant_to_string(imp, variables, True))

    return " | ".join(dnf_terms)


def calculated_method_cnf(table, verbose=True):
    if not table:
        return "1"
    variables = sorted(table[0][0].keys())
    terms = []
    for row, val in table:
        if not val:
            t = _get_binary_representation(row, variables)
            terms.append(t)

    if not terms:
        return "1"

    prime_implicants = _quine_mccluskey(terms, verbose)
    essential_implicants = _minimize_cover(prime_implicants, terms, verbose)

    if not essential_implicants:
        return "1"

    for imp in essential_implicants:
        if all(x is None for x in imp):
            return "0"

    cnf_terms = []
    for imp in essential_implicants:
        cnf_terms.append(_implicant_to_string(imp, variables, False))

    return " & ".join(cnf_terms)
