import numpy as np
from itertools import product, chain, combinations
from collections import defaultdict

def _get_binary_representation(row, variables_order):
    return tuple(row[v] for v in variables_order)


def _weight(term):
    return sum(1 for x in term if x == 1)


def _covers(implicant, term):
    for i in range(len(implicant)):
        if implicant[i] is not None and implicant[i] != term[i]:
            return False
    return True


def _quine_mccluskey(terms, verbose=True):
    if not terms:
        return []
    n = len(terms[0])
    prime_implicants = []
    current_terms = terms
    stage = 0

    if verbose:
        print("Этап 0:")
        groups0 = {}
        for t in current_terms:
            w = _weight(t)
            groups0.setdefault(w, []).append(t)
        for w in sorted(groups0):
            print(f"Группа {w}: {groups0[w]}")

    while current_terms:
        stage += 1
        groups = {}
        for i, t in enumerate(current_terms):
            w = _weight(t)
            groups.setdefault(w, []).append((t, i))

        next_terms = []
        merged_indices = set()
        sorted_weights = sorted(groups.keys())

        for i in range(len(sorted_weights) - 1):
            w1 = sorted_weights[i]
            w2 = sorted_weights[i + 1]
            if w2 - w1 != 1:
                continue
            for (t1, idx1) in groups[w1]:
                for (t2, idx2) in groups[w2]:
                    diff_count = 0
                    diff_pos = None
                    for k in range(n):
                        if t1[k] != t2[k]:
                            diff_count += 1
                            diff_pos = k
                            if diff_count > 1:
                                break
                    if diff_count == 1:
                        new_term = list(t1)
                        new_term[diff_pos] = None
                        new_term = tuple(new_term)
                        merged_indices.add(idx1)
                        merged_indices.add(idx2)
                        if new_term not in next_terms:
                            next_terms.append(new_term)

        for i, t in enumerate(current_terms):
            if i not in merged_indices:
                if t not in prime_implicants:
                    prime_implicants.append(t)

        if verbose and next_terms:
            print(f"Этап {stage}:")
            next_groups = {}
            for t in next_terms:
                w = _weight(t)
                next_groups.setdefault(w, []).append(t)
            for w in sorted(next_groups):
                print(f"Группа {w}: {next_groups[w]}")

        current_terms = next_terms

    return prime_implicants


def _minimize_cover(prime_implicants, terms, verbose=True):
    if not terms or not prime_implicants:
        return []
    n_terms = len(terms)
    cover_sets = []
    for imp in prime_implicants:
        cover_set = set()
        for j, term in enumerate(terms):
            if _covers(imp, term):
                cover_set.add(j)
        cover_sets.append(cover_set)

    uncovered = set(range(n_terms))
    solution_inds = []

    while uncovered:
        best_imp_idx = None
        best_cover = set()
        for i, cover_set in enumerate(cover_sets):
            if i in solution_inds:
                continue
            cover = cover_set & uncovered
            if len(cover) > len(best_cover):
                best_cover = cover
                best_imp_idx = i
        if best_imp_idx is None:
            break
        solution_inds.append(best_imp_idx)
        uncovered -= best_cover

    return [prime_implicants[i] for i in solution_inds]


def _implicant_to_string(implicant, variables, is_dnf):
    parts = []
    for i, var in enumerate(variables):
        if implicant[i] is not None:
            if is_dnf:
                if implicant[i] == 0:
                    parts.append(f"!{var}")
                else:
                    parts.append(var)
            else:
                if implicant[i] == 0:
                    parts.append(var)
                else:
                    parts.append(f"!{var}")
    if not parts:
        return "1" if is_dnf else "0"
    if is_dnf:
        return f'({" & ".join(parts)})'
    else:
        return f'({" | ".join(parts)})'


def _quine_mccluskey(terms, verbose=True):
    """Реализует алгоритм Квайна-МакКласки для поиска первичных импликант."""
    if not terms:
        return []
    n = len(terms[0])
    current_terms = terms
    prime_implicants = []
    stage = 0

    if verbose:
        print("Этап 0:")
        groups0 = {}
        for t in current_terms:
            w = _weight(t)
            groups0.setdefault(w, []).append(t)
        for w in sorted(groups0):
            print(f"  Группа {w}: {groups0[w]}")

    while current_terms:
        groups = {}
        for idx, t in enumerate(current_terms):
            w = _weight(t)
            groups.setdefault(w, []).append((t, idx))

        next_terms = []
        merged = [False] * len(current_terms)
        sorted_weights = sorted(groups.keys())

        for i in range(len(sorted_weights) - 1):
            w1 = sorted_weights[i]
            w2 = sorted_weights[i + 1]
            if w2 - w1 != 1:
                continue
            for t1, idx1 in groups[w1]:
                for t2, idx2 in groups[w2]:
                    diff_count = 0
                    diff_pos = -1
                    for k in range(n):
                        if t1[k] != t2[k]:
                            diff_count += 1
                            diff_pos = k
                            if diff_count > 1:
                                break
                    if diff_count == 1:
                        new_term = list(t1)
                        new_term[diff_pos] = None
                        new_term = tuple(new_term)
                        merged[idx1] = True
                        merged[idx2] = True
                        if new_term not in next_terms:
                            next_terms.append(new_term)

        for i, t in enumerate(current_terms):
            if not merged[i]:
                if t not in prime_implicants:
                    prime_implicants.append(t)

        if next_terms and verbose:
            stage += 1
            print(f"Этап {stage}:")
            next_groups = {}
            for t in next_terms:
                w = _weight(t)
                next_groups.setdefault(w, []).append(t)
            for w in sorted(next_groups):
                print(f"  Группа {w}: {next_groups[w]}")

        current_terms = next_terms

    return prime_implicants


def _minimize_cover(prime_implicants, terms, verbose=True):
    """Минимизирует покрытие с помощью жадного алгоритма и выводит таблицу покрытия."""
    if not prime_implicants or not terms:
        return []

    if verbose:
        header = "      "
        for term in terms:
            header += f"  {term}   "
        print(header)

        for imp in prime_implicants:
            row = f"{str(imp):6}|"
            for term in terms:
                if _covers(imp, term):
                    row += "   V   "
                else:
                    row += "       "
            print(row)

    cover_sets = []
    for imp in prime_implicants:
        cover_set = set()
        for j, term in enumerate(terms):
            if _covers(imp, term):
                cover_set.add(j)
        cover_sets.append(cover_set)

    uncovered = set(range(len(terms)))
    cover_indices = []

    while uncovered:
        best_idx = None
        best_cover = set()
        for i, cov_set in enumerate(cover_sets):
            current_cover = cov_set & uncovered
            if len(current_cover) > len(best_cover):
                best_cover = current_cover
                best_idx = i
        if best_idx is None:
            break
        cover_indices.append(best_idx)
        uncovered -= best_cover

    return [prime_implicants[i] for i in cover_indices]

# Преобразование значения в 0/1
def to_binary(val):
    if isinstance(val, bool):
        return 1 if val else 0
    return 1 if val else 0


# Получение всех подмножеств (кроме пустого)
def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))


# Коды Грея для 2 переменных
gray_codes_2 = {
    (0, 0): 0,
    (0, 1): 1,
    (1, 1): 2,
    (1, 0): 3
}

# Обратное преобразование индекса в комбинацию
gray_index_to_comb = {
    0: (0, 0),
    1: (0, 1),
    2: (1, 1),
    3: (1, 0)
}


# Построение карты Карно
def build_kmap(table):
    if not table:
        return None, []

    # Получаем переменные и сортируем
    variables = sorted(table[0][0].keys())
    n = len(variables)

    # Инициализация карты в зависимости от количества переменных
    if n == 0:
        return None, []
    elif n == 1:
        kmap = np.zeros((1, 2), dtype=int)
    elif n == 2:
        kmap = np.zeros((2, 2), dtype=int)
    elif n == 3:
        kmap = np.zeros((2, 4), dtype=int)
    elif n == 4:
        kmap = np.zeros((4, 4), dtype=int)
    elif n == 5:
        kmap = [np.zeros((4, 4), dtype=int), np.zeros((4, 4), dtype=int)]
    else:
        raise ValueError("До 5 переменных")

    # Заполняем карту
    for row, val in table:
        vals = [row[v] for v in variables]
        bin_val = to_binary(val)

        if n == 1:
            kmap[0, vals[0]] = bin_val
        elif n == 2:
            kmap[vals[0], vals[1]] = bin_val
        elif n == 3:
            a = vals[0]
            bc = (vals[1], vals[2])
            col = gray_codes_2[bc]
            kmap[a, col] = bin_val
        elif n == 4:
            ab = (vals[0], vals[1])
            cd = (vals[2], vals[3])
            row_idx = gray_codes_2[ab]
            col_idx = gray_codes_2[cd]
            kmap[row_idx, col_idx] = bin_val
        elif n == 5:
            a = vals[0]
            bc = (vals[1], vals[2])
            de = (vals[3], vals[4])
            row_idx = gray_codes_2[bc]
            col_idx = gray_codes_2[de]
            kmap[a][row_idx, col_idx] = bin_val

    return kmap, variables


# Проверка, является ли набор непрерывным прямоугольником
def is_continuous_rect(indices, size):
    if not indices:
        return False

    indices = sorted(indices)
    # Проверка непрерывности с учетом цикличности
    if all((indices[i] + 1) % size == indices[i + 1] for i in range(len(indices) - 1)):
        return True
    # Проверка непрерывности с оберткой
    if indices[0] == 0 and indices[-1] == size - 1:
        return all(i in indices for i in range(indices[0], size)) and \
            all(i in indices for i in range(0, indices[-1] + 1))
    return False


# Поиск всех прямоугольников в карте
def find_rectangles(kmap, n_vars, target=1):
    rectangles = []

    if n_vars <= 4:
        # 2D карта
        if n_vars == 1:
            rows, cols = 1, 2
        elif n_vars == 2:
            rows, cols = 2, 2
        elif n_vars == 3:
            rows, cols = 2, 4
        else:  # n_vars == 4
            rows, cols = 4, 4

        kmap_2d = kmap

        # Исправлено: убрана лишняя скобка после range(cols)
        for row_set in powerset(range(rows)):
            for col_set in powerset(range(cols)):
                if not is_continuous_rect(row_set, rows) or not is_continuous_rect(col_set, cols):
                    continue

                # Проверяем все клетки в прямоугольнике
                valid = True
                for r in row_set:
                    for c in col_set:
                        if kmap_2d[r, c] != target:
                            valid = False
                            break
                    if not valid:
                        break

                if valid:
                    rectangles.append((set(), set(row_set), set(col_set)))

    elif n_vars == 5:
        # 3D карта (A, BC, DE)
        for a_set in powerset([0, 1]):
            a_set = set(a_set)
            for row_set in powerset(range(4)):
                for col_set in powerset(range(4)):
                    if not is_continuous_rect(row_set, 4) or not is_continuous_rect(col_set, 4):
                        continue

                    valid = True
                    for a in a_set:
                        for r in row_set:
                            for c in col_set:
                                if kmap[a][r, c] != target:
                                    valid = False
                                    break
                            if not valid:
                                break
                        if not valid:
                            break

                    if valid:
                        rectangles.append((a_set, set(row_set), set(col_set)))

    return rectangles


# Фильтрация максимальных прямоугольников
def filter_max_rectangles(rectangles):
    max_rects = []
    for rect in rectangles:
        a_set, rows, cols = rect
        is_max = True
        for other in rectangles:
            a_other, rows_other, cols_other = other
            if a_set.issubset(a_other) and rows.issubset(rows_other) and cols.issubset(cols_other) and rect != other:
                is_max = False
                break
        if is_max:
            max_rects.append(rect)
    return max_rects


# Жадное покрытие
def greedy_cover(kmap, rectangles, n_vars, target=1):
    covered = set()
    to_cover = set()

    # Собираем все клетки, которые нужно покрыть
    if n_vars <= 4:
        if n_vars == 1:
            for c in range(2):
                if kmap[0, c] == target:
                    to_cover.add(("2D", 0, c))
        elif n_vars == 2:
            for r in range(2):
                for c in range(2):
                    if kmap[r, c] == target:
                        to_cover.add(("2D", r, c))
        elif n_vars == 3:
            for r in range(2):
                for c in range(4):
                    if kmap[r, c] == target:
                        to_cover.add(("2D", r, c))
        elif n_vars == 4:
            for r in range(4):
                for c in range(4):
                    if kmap[r, c] == target:
                        to_cover.add(("2D", r, c))
    elif n_vars == 5:
        for a in [0, 1]:
            for r in range(4):
                for c in range(4):
                    if kmap[a][r, c] == target:
                        to_cover.add(("3D", a, r, c))

    selected = []
    while to_cover:
        best_rect = None
        best_cover = set()
        for rect in rectangles:
            a_set, rows, cols = rect
            cover = set()
            if n_vars <= 4:
                for r in rows:
                    for c in cols:
                        if ("2D", r, c) in to_cover:
                            cover.add(("2D", r, c))
            elif n_vars == 5:
                for a in a_set:
                    for r in rows:
                        for c in cols:
                            if ("3D", a, r, c) in to_cover:
                                cover.add(("3D", a, r, c))
            if len(cover) > len(best_cover):
                best_cover = cover
                best_rect = rect
        if best_rect is None:
            break
        selected.append(best_rect)
        to_cover -= best_cover
        rectangles.remove(best_rect)

    return selected


# Преобразование прямоугольника в терм
def rect_to_term(rect, variables, for_dnf=True):
    a_set, rows, cols = rect
    n_vars = len(variables)
    term = []

    if n_vars == 1:
        if len(rows) == 1 and len(cols) == 2:  # Вся строка
            return "" if for_dnf else f"{variables[0]} | ~{variables[0]}"
        if 0 in cols:
            term.append(f"~{variables[0]}" if for_dnf else variables[0])
        if 1 in cols:
            term.append(variables[0] if for_dnf else f"~{variables[0]}")

    elif n_vars == 2:
        if len(rows) == 2:  # Все значения A
            pass
        elif 0 in rows:
            term.append(f"~{variables[0]}" if for_dnf else variables[0])
        elif 1 in rows:
            term.append(variables[0] if for_dnf else f"~{variables[0]}")

        if len(cols) == 2:  # Все значения B
            pass
        elif 0 in cols:
            term.append(f"~{variables[1]}" if for_dnf else variables[1])
        elif 1 in cols:
            term.append(variables[1] if for_dnf else f"~{variables[1]}")

    elif n_vars == 3:
        # A (строки)
        if len(rows) == 2:  # Все A
            pass
        elif 0 in rows:
            term.append(f"~{variables[0]}" if for_dnf else variables[0])
        elif 1 in rows:
            term.append(variables[0] if for_dnf else f"~{variables[0]}")

        # BC (столбцы)
        if len(cols) == 4:  # Все BC
            pass
        else:
            bc_vals = [gray_index_to_comb[c] for c in cols]
            b_vals = set(b for b, c in bc_vals)
            c_vals = set(c for b, c in bc_vals)

            if len(b_vals) == 1:
                b_val = next(iter(b_vals))
                term.append(f"~{variables[1]}" if b_val == 0 and for_dnf else variables[1])
                term.append(variables[1] if b_val == 1 and for_dnf else f"~{variables[1]}")
            if len(c_vals) == 1:
                c_val = next(iter(c_vals))
                term.append(f"~{variables[2]}" if c_val == 0 and for_dnf else variables[2])
                term.append(variables[2] if c_val == 1 and for_dnf else f"~{variables[2]}")

    elif n_vars == 4:
        # AB (строки)
        if len(rows) == 4:  # Все AB
            pass
        else:
            ab_vals = [gray_index_to_comb[r] for r in rows]
            a_vals = set(a for a, b in ab_vals)
            b_vals = set(b for a, b in ab_vals)

            if len(a_vals) == 1:
                a_val = next(iter(a_vals))
                term.append(f"~{variables[0]}" if a_val == 0 and for_dnf else variables[0])
                term.append(variables[0] if a_val == 1 and for_dnf else f"~{variables[0]}")
            if len(b_vals) == 1:
                b_val = next(iter(b_vals))
                term.append(f"~{variables[1]}" if b_val == 0 and for_dnf else variables[1])
                term.append(variables[1] if b_val == 1 and for_dnf else f"~{variables[1]}")

        # CD (столбцы)
        if len(cols) == 4:  # Все CD
            pass
        else:
            cd_vals = [gray_index_to_comb[c] for c in cols]
            c_vals = set(c for c, d in cd_vals)
            d_vals = set(d for c, d in cd_vals)

            if len(c_vals) == 1:
                c_val = next(iter(c_vals))
                term.append(f"~{variables[2]}" if c_val == 0 and for_dnf else variables[2])
                term.append(variables[2] if c_val == 1 and for_dnf else f"~{variables[2]}")
            if len(d_vals) == 1:
                d_val = next(iter(d_vals))
                term.append(f"~{variables[3]}" if d_val == 0 and for_dnf else variables[3])
                term.append(variables[3] if d_val == 1 and for_dnf else f"~{variables[3]}")

    elif n_vars == 5:
        # A
        if len(a_set) == 2:  # Охватывает обе карты
            pass
        elif 0 in a_set:
            term.append(f"~{variables[0]}" if for_dnf else variables[0])
        elif 1 in a_set:
            term.append(variables[0] if for_dnf else f"~{variables[0]}")

        # BC (строки)
        if len(rows) == 4:  # Все BC
            pass
        else:
            bc_vals = [gray_index_to_comb[r] for r in rows]
            b_vals = set(b for b, c in bc_vals)
            c_vals = set(c for b, c in bc_vals)

            if len(b_vals) == 1:
                b_val = next(iter(b_vals))
                term.append(f"~{variables[1]}" if b_val == 0 and for_dnf else variables[1])
                term.append(variables[1] if b_val == 1 and for_dnf else f"~{variables[1]}")
            if len(c_vals) == 1:
                c_val = next(iter(c_vals))
                term.append(f"~{variables[2]}" if c_val == 0 and for_dnf else variables[2])
                term.append(variables[2] if c_val == 1 and for_dnf else f"~{variables[2]}")

        # DE (столбцы)
        if len(cols) == 4:  # Все DE
            pass
        else:
            de_vals = [gray_index_to_comb[c] for c in cols]
            d_vals = set(d for d, e in de_vals)
            e_vals = set(e for d, e in de_vals)

            if len(d_vals) == 1:
                d_val = next(iter(d_vals))
                term.append(f"~{variables[3]}" if d_val == 0 and for_dnf else variables[3])
                term.append(variables[3] if d_val == 1 and for_dnf else f"~{variables[3]}")
            if len(e_vals) == 1:
                e_val = next(iter(e_vals))
                term.append(f"~{variables[4]}" if e_val == 0 and for_dnf else variables[4])
                term.append(variables[4] if e_val == 1 and for_dnf else f"~{variables[4]}")

    return term


# Вывод карты Карно
def print_kmap(kmap, n_vars):
    if n_vars == 0:
        return
    print("\nКарта Карно:")
    if n_vars == 1:
        print("   A=0 | A=1")
        print(f"   {kmap[0, 0]}    | {kmap[0, 1]}")
    elif n_vars == 2:
        print("     B=0 | B=1")
        print(f"A=0   {kmap[0, 0]}   | {kmap[0, 1]}")
        print(f"A=1   {kmap[1, 0]}   | {kmap[1, 1]}")
    elif n_vars == 3:
        print("     BC:00 01 11 10")
        for i in range(2):
            print(f"A={i}   ", end="")
            for j in range(4):
                print(f" {kmap[i, j]} ", end="")
            print()
    elif n_vars == 4:
        print("     CD:00 01 11 10")
        ab_labels = ["AB=00", "AB=01", "AB=11", "AB=10"]
        for i, label in enumerate(ab_labels):
            print(f"{label} ", end="")
            for j in range(4):
                print(f" {kmap[i, j]} ", end="")
            print()
    elif n_vars == 5:
        print("A=0:")
        print("     DE:00 01 11 10")
        bc_labels = ["BC=00", "BC=01", "BC=11", "BC=10"]
        for i, label in enumerate(bc_labels):
            print(f"{label} ", end="")
            for j in range(4):
                print(f" {kmap[0][i, j]} ", end="")
            print()
        print("\nA=1:")
        print("     DE:00 01 11 10")
        for i, label in enumerate(bc_labels):
            print(f"{label} ", end="")
            for j in range(4):
                print(f" {kmap[1][i, j]} ", end="")
            print()