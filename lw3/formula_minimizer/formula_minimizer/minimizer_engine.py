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