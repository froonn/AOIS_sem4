from .minimizer_engine import *


def optimize_kmap(terms_list: list, labels: list, use_conjunctive: bool = True) -> list:
    num_vars = len(labels)

    bin_sequences = translate_to_binary_sequence(terms_list, num_vars)
    core_components = determine_prime_components(bin_sequences, num_vars)
    key_components = pick_critical_components(core_components, bin_sequences)

    op_symbol = '&' if use_conjunctive else '|'
    logical_expressions = []

    for component in key_components:
        parts = []
        for lbl, bit_value in zip(labels, component):
            if bit_value == '-':
                continue

            if use_conjunctive:
                parts.append(lbl if bit_value else f"!{lbl}")
            else:
                parts.append(f"!{lbl}" if bit_value else lbl)

        if parts:
            logical_expressions.append(f"({op_symbol.join(parts)})")
        else:
            logical_expressions.append("1" if use_conjunctive else "0")

    return logical_expressions