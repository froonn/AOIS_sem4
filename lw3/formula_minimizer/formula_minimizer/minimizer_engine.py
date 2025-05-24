def process_with_table_method(input_terms, bit_size, symbols, disj_form=True):
    """Реализует табличный метод обработки"""
    if not isinstance(input_terms, (list, set)):
        raise TypeError("Input must be collection of terms")
    if not isinstance(bit_size, int) or bit_size <= 0:
        raise ValueError("Positive bit length required")
    if not isinstance(symbols, list) or len(symbols) != bit_size:
        raise ValueError("Symbol list mismatch")

    core_implicants = calculate_core_terms(input_terms, bit_size, symbols, disj_form)
    coverage_chart = build_coverage_chart(core_implicants, input_terms, bit_size, symbols, disj_form)
    show_coverage_matrix(coverage_chart, input_terms, symbols, disj_form)
    return core_implicants


def build_coverage_chart(core_implicants, term_list, bit_size, symbols,
                         disj_form=True):
    """Создает матрицу покрытия"""
    if not isinstance(core_implicants, (list, set)):
        raise TypeError("Requires core components collection")
    return {
        comp: ["X" if check_component_coverage(comp, integer_to_binary_string(n, bit_size)) else "."
               for n in term_list]
        for comp in core_implicants
    }


def show_coverage_matrix(matrix, term_collection, symbols, disj_form=True):
    """Визуализирует матрицу покрытия"""
    header = [transform_term_to_logical(n, symbols, not disj_form).replace(" ", "_")
              for n in term_collection]
    print("\nCoverage Matrix:\n" + " " * 25 + " ".join(f"{cell:18}" for cell in header))

    for comp in sorted(matrix.keys(), key=lambda x: x.count('-')):
        expr = binary_to_expression(comp, symbols, disj_form)
        print(f"{expr:25} | " + " ".join(f"{('X' if c == 'X' else '.'):18}"
                                         for c in matrix[comp]))


def transform_term_to_logical(term_index, symbols, for_conj=True):
    """Преобразует индекс в логическое выражение"""
    bin_pattern = format(term_index, f'0{len(symbols)}b')
    parts = [
        ("!" + v if b == '1' else v) if for_conj
        else (v if b == '1' else "!" + v)
        for b, v in zip(bin_pattern, symbols)
    ]
    return f"({('|' if for_conj else '&').join(parts)})"


def translate_to_binary_sequence(input_numbers: list, bit_length: int) -> list:
    """Преобразует числа в бинарные последовательности"""
    max_val = 1 << bit_length
    if any(n >= max_val for n in input_numbers):
        raise ValueError("Number exceeds bit capacity")
    return [tuple((n >> i) & 1 for i in reversed(range(bit_length)))
            for n in input_numbers]


def determine_prime_components(binary_sequences: list, bit_size: int) -> set:
    """Определяет основные компоненты"""
    categorized_terms = {}
    for seq in binary_sequences:
        key = seq.count(1)
        categorized_terms.setdefault(key, []).append(seq)

    pending_terms = set(binary_sequences)
    prime_components = set()

    while categorized_terms:
        next_group = {}
        handled = set()
        for key in sorted(categorized_terms):
            for t1 in categorized_terms[key]:
                for t2 in categorized_terms.get(key + 1, []):
                    merged = merge_term_pairs(t1, t2)
                    if merged:
                        handled.update({t1, t2})
                        next_group.setdefault(merged.count(1), []).append(merged)

        prime_components.update(pending_terms - handled)
        categorized_terms = {k: v for k, v in next_group.items() if v}

    return prime_components


def merge_term_pairs(first_term: tuple, second_term: tuple) -> tuple:
    """Объединяет пары терминов"""
    diff = 0
    result = []
    for a, b in zip(first_term, second_term):
        result.append(a if a == b else '-')
        diff += (a != b)
    return tuple(result) if diff == 1 else None


def pick_critical_components(core_set: set, minimal_terms: list) -> set:
    """Выбирает ключевые компоненты"""
    coverage_data = {comp: [mt for mt in minimal_terms
                            if check_component_coverage(comp, mt)] for comp in core_set}

    essential = {next(iter([c for c in core_set if mt in coverage_data[c]]))
                 for mt in minimal_terms if len([c for c in core_set
                                                 if mt in coverage_data[c]]) == 1}

    remaining = set(minimal_terms) - {mt for c in essential for mt in coverage_data[c]}
    while remaining:
        best = max(coverage_data.items(),
                   key=lambda x: len(set(x[1]) & remaining))
        essential.add(best[0])
        remaining -= set(best[1])

    return essential


def check_component_coverage(component: tuple, target_term: tuple) -> bool:
    """Проверяет покрытие компонента"""
    return all(c == '-' or c == t for c, t in zip(component, target_term))

def integer_to_binary_string(num: int, bits: int) -> str:
    if not isinstance(num, int) or num < 0:
        raise ValueError("Input number should be non-negative integer")
    if not isinstance(bits, int) or bits <= 0:
        raise ValueError("Bit count must be positive integer")

    max_val = 1 << bits
    if num >= max_val:
        raise ValueError(f"Number {num} exceeds {bits}-bit capacity")

    return f"{num:0{bits}b}"


def combine_terms(term1: str, term2: str) -> str | None:
    if not isinstance(term1, str) or not isinstance(term2, str):
        raise TypeError("Terms should be string type")
    if len(term1) != len(term2):
        raise ValueError("Terms length mismatch")

    valid_chars = {'0', '1', '-'}
    if any(c not in valid_chars for c in term1):
        raise ValueError("Invalid characters in first term")
    if any(c not in valid_chars for c in term2):
        raise ValueError("Invalid characters in second term")

    diff_count = 0
    merged_bits = []
    for b1, b2 in zip(term1, term2):
        if b1 != b2:
            diff_count += 1
            merged_bits.append('-')
        else:
            merged_bits.append(b1)

    return ''.join(merged_bits) if diff_count == 1 else None


def binary_to_expression(pattern: str, vars_list: list,
                         is_and_operation: bool) -> str:
    if not isinstance(pattern, str):
        raise TypeError("Pattern must be string type")
    if not isinstance(vars_list, list):
        raise TypeError("Variable list required")
    if len(pattern) != len(vars_list):
        raise ValueError("Pattern/variable count mismatch")
    if any(c not in {'0', '1', '-'} for c in pattern):
        raise ValueError("Invalid pattern symbols")
    if not all(isinstance(v, str) for v in vars_list):
        raise ValueError("Variables must be strings")

    parts = []
    for bit, var_name in zip(pattern, vars_list):
        if bit == '-':
            continue

        # XOR condition for negation
        needs_not = (bit == '1') ^ (not is_and_operation)
        parts.append(f"!{var_name}" if needs_not else var_name)

    op_symbol = '&' if is_and_operation else '|'
    joined = op_symbol.join(parts)
    return joined if joined else ('1' if is_and_operation else '0')


def get_literal_set(pattern: str, vars_list: list,
                    as_conjunction: bool) -> set:
    if not isinstance(pattern, str):
        raise TypeError("Pattern must be string")
    if len(pattern) != len(vars_list):
        raise ValueError("Pattern-variable length mismatch")

    return {
        f"{'' if (bit == '1') ^ (not as_conjunction) else '!'}{var_name}"
        for bit, var_name in zip(pattern, vars_list) if bit != '-'
    }


def check_implicant_coverage(imp: str, term: str) -> bool:
    if len(imp) != len(term):
        raise ValueError("Length mismatch between implicant and term")

    return all(i_bit == '-' or i_bit == t_bit
               for i_bit, t_bit in zip(imp, term))


def remove_redundant_terms(primes: list, terms_list: list,
                           num_bits: int) -> list:
    active_terms = primes.copy()
    changed = True

    while changed:
        changed = False
        for term in active_terms.copy():
            # Create temporary list without current term
            temp_list = [t for t in active_terms if t != term]

            # Check if all minterms are covered by remaining terms
            all_covered = True
            for minterm in terms_list:
                bin_str = format(minterm, f'0{num_bits}b')
                if not any(check_implicant_coverage(t, bin_str) for t in temp_list):
                    all_covered = False
                    break

            if all_covered:
                active_terms.remove(term)
                changed = True

    return active_terms


def find_essential_implicants(primes: list, vars_list: list,
                              as_conjunction: bool) -> list:
    imp_data = [
        (imp, get_literal_set(imp, vars_list, as_conjunction))
        for imp in primes
    ]
    essential_terms = []

    for idx, (current_term, current_literals) in enumerate(imp_data):
        has_subset = False
        for other_idx, (_, other_lits) in enumerate(imp_data):
            if idx == other_idx:
                continue
            if other_lits.issubset(current_literals):
                has_subset = True
                break

        if not has_subset:
            essential_terms.append(current_term)

    return essential_terms


def find_critical_terms(core_terms, term_list, bit_size, labels,
                        disj_form=True):
    if not isinstance(core_terms, (list, set)):
        raise TypeError("Requires term collection")
    if not isinstance(term_list, (list, set)):
        raise TypeError("Invalid terms format")
    if not isinstance(bit_size, int) or bit_size <= 0:
        raise ValueError("Invalid bit quantity")
    if not isinstance(labels, list) or len(labels) != bit_size:
        raise ValueError("Label mismatch")

    return core_terms if disj_form else [
        current_term for current_term in core_terms if not any(
            get_literal_set(current_term, labels, disj_form).issubset(
                get_literal_set(other_term, labels, disj_form)
            ) for other_term in core_terms if current_term != other_term
        )
    ]


def calculate_core_terms(terms_list, bit_size, labels, disj_form=True):
    if not isinstance(terms_list, (list, set)):
        raise TypeError("Requires collection of terms")
    if not isinstance(bit_size, int) or bit_size <= 0:
        raise ValueError("Positive bit quantity required")
    if not isinstance(labels, list) or len(labels) != bit_size:
        raise ValueError("Label list size mismatch")
    if any(not isinstance(n, int) or n < 0 for n in terms_list):
        raise ValueError("Negative values not allowed")
    if any(n >= (1 << bit_size) for n in terms_list):
        raise ValueError("Value exceeds bit capacity")

    category_map = {}
    for num in terms_list:
        bin_repr = integer_to_binary_string(num, bit_size)
        active_bits = bin_repr.count('1')
        category_map.setdefault(active_bits, set()).add(bin_repr)

    print("\n=== Этап объединения: Начальные группы ===")
    for cnt in sorted(category_map):
        elements = sorted(category_map[cnt])
        print(f"Категория {cnt}: " + ", ".join(
            binary_to_expression(e, labels, disj_form) for e in elements))

    phase = 1
    core_results = []
    while True:
        updated_map = {}
        used_terms = set()
        sorted_counts = sorted(category_map.keys())

        for i in range(len(sorted_counts) - 1):
            for first_term in category_map[sorted_counts[i]]:
                for second_term in category_map[sorted_counts[i + 1]]:
                    combined = combine_terms(first_term, second_term)
                    if combined:
                        updated_map.setdefault(combined.count('1'), set()).add(combined)
                        used_terms.update({first_term, second_term})

        core_results.extend(t for k in category_map for t in category_map[k] if t not in used_terms)

        if not updated_map:
            print(f"\n=== Завершено на фазе {phase} ===")
            break

        print(f"\n=== Фаза {phase} ===")
        for key in sorted(updated_map.keys()):
            items = sorted(updated_map[key])
            print(f"Категория {key}: " + ", ".join(
                binary_to_expression(x, labels, disj_form) for x in items))

        phase += 1
        category_map = updated_map

    return sorted(set(core_results))
