import io
from functools import cmp_to_key

class Term:
    def __init__(self, vars_str):
        self.vars = vars_str
        self.used = False
        self.covered_terms = {vars_str}

def can_glue(t1: str, t2: str, var_count: int) -> bool:
    diff = 0
    for i in range(var_count):
        if t1[i] != t2[i]:
            diff += 1
        if diff > 1:
            return False
    return diff == 1

def glue(t1: str, t2: str) -> str:
    result = list(t1)
    for i in range(len(t1)):
        if t1[i] != t2[i]:
            result[i] = '-'
    return "".join(result)

def format_dnf_term(term: str, var_names: list[str]) -> str:
    result = []
    for i, char in enumerate(term):
        if char == '-':
            continue
        if char == '0':
            result.append(f"!{var_names[i]}")
        elif char == '1':
            result.append(var_names[i])
    return "&".join(result) if result else "1"

def glue_terms(terms: list[Term], var_names: list[str]) -> list[Term]:
    print("Стадия склеивания:")
    var_count = len(var_names)
    glued = True
    while glued:
        glued = False
        new_terms_set = set()
        used = [False] * len(terms)
        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                if can_glue(terms[i].vars, terms[j].vars, var_count):
                    glued_term_str = glue(terms[i].vars, terms[j].vars)
                    new_terms_set.add(glued_term_str)
                    used[i] = used[j] = True
                    glued = True
                    print(f"({format_dnf_term(terms[i].vars, var_names)}) | "
                          f"({format_dnf_term(terms[j].vars, var_names)}) => "
                          f"({format_dnf_term(glued_term_str, var_names)})")
        for i in range(len(terms)):
            if not used[i]:
                new_terms_set.add(terms[i].vars)
        terms = [Term(t) for t in new_terms_set]
    return terms

def parse_dnf_term(term: str, var_names: list[str]) -> str:
    result = ['-'] * len(var_names)
    current_term_literals = []

    i = 0
    while i < len(term):
        if term[i] == '!':
            var = term[i + 1]
            current_term_literals.append((var, '0'))
            i += 2
        elif term[i].isalpha():
            var = term[i]
            current_term_literals.append((var, '1'))
            i += 1
        else:
            i += 1
            continue

    for literal_var, state in current_term_literals:
        try:
            index = var_names.index(literal_var)
            result[index] = state
        except ValueError:
            pass

    return "".join(result)

def _custom_char_sort_key(a, b):
    return (a > b) - (a < b)

def parse_function(input_str: str, var_names: list[str]) -> list[Term]:
    terms = []
    var_names.clear()
    unique_vars_set = set()

    temp_terms_str = input_str.split('|')
    for temp_term in temp_terms_str:
        temp_term = temp_term.replace(' ', '')
        if not temp_term:
            continue
        for char in temp_term:
            if char.isalpha():
                unique_vars_set.add(char)

    var_names.extend(sorted(list(unique_vars_set), key=cmp_to_key(_custom_char_sort_key)))

    for term_str in temp_terms_str:
        term_str = term_str.replace(' ', '')
        if not term_str:
            continue

        parsed_binary_term = ['-'] * len(var_names)

        pos = 0
        while pos < len(term_str):
            literal_char = ''
            value = ''

            if term_str[pos] == '!':
                literal_char = term_str[pos + 1]
                value = '0'
                pos += 2
            elif term_str[pos].isalpha():
                literal_char = term_str[pos]
                value = '1'
                pos += 1
            else:
                pos += 1
                continue

            try:
                index = var_names.index(literal_char)
                parsed_binary_term[index] = value
            except ValueError:
                pass

        t = Term("".join(parsed_binary_term))
        t.covered_terms.add("".join(parsed_binary_term))
        terms.append(t)
    return terms

def build_adder():
    print("\n=== Одноразрядный двоичный сумматор на 3 входа ===")
    var_names = ['A', 'B', 'C']
    sdnf_S, sdnf_Cout = [], []

    print("Таблица истинности:")
    print("A B C | S Cout")
    print("------+-------")
    for A in range(2):
        for B in range(2):
            for C in range(2):
                s = A + B + C
                S = s % 2
                Cout = s // 2
                print(f"{A} {B} {C} | {S} {Cout}")

                term_prefix = ""
                term_prefix += ('1' if A else '0')
                term_prefix += ('1' if B else '0')
                term_prefix += ('1' if C else '0')

                if S == 1:
                    sdnf_S.append(term_prefix)
                if Cout == 1:
                    sdnf_Cout.append(term_prefix)

    sdnf_S_str = "|".join([f"({format_dnf_term(term, var_names)})" for term in sdnf_S])
    print(f"\nСДНФ для S: {sdnf_S_str}")

    terms_S = [Term(bin_term) for bin_term in sdnf_S]
    minimized_S = glue_terms(terms_S, var_names)

    print("Минимизированная форма S: ", end="")
    minimized_S_formatted = [f"({format_dnf_term(term.vars, var_names)})" for term in minimized_S]
    print("|".join(minimized_S_formatted))

    sdnf_Cout_str = "|".join([f"({format_dnf_term(term, var_names)})" for term in sdnf_Cout])
    print(f"\nСДНФ для Cout: {sdnf_Cout_str}")

    terms_Cout = [Term(bin_term) for bin_term in sdnf_Cout]
    minimized_Cout = glue_terms(terms_Cout, var_names)

    print("Минимизированная форма Cout: ", end="")
    minimized_Cout_formatted = [f"({format_dnf_term(term.vars, var_names)})" for term in minimized_Cout]
    print("|".join(minimized_Cout_formatted))
    print("")

def to_bcd(decimal: int) -> list[int]:
    decimal = decimal % 10
    bcd = [0] * 4
    bcd[0] = (decimal >> 3) & 1
    bcd[1] = (decimal >> 2) & 1
    bcd[2] = (decimal >> 1) & 1
    bcd[3] = decimal & 1
    return bcd

def print_bcd_converter_table_and_dnf():
    print("\n=== Преобразователь Д8421 в Д8421+6 ===")
    var_names = ['A', 'B', 'C', 'D']
    sdnf_Y1, sdnf_Y2, sdnf_Y3, sdnf_Y4 = [], [], [], []

    print("D8421\t\tD8421+6")
    print("A B C D\t\tY1 Y2 Y3 Y4")
    print("--------------------------")

    for i in range(10):
        bits = to_bcd(i)
        A, B, C, D = bits[0], bits[1], bits[2], bits[3]
        term_binary_input = ""
        term_binary_input += ('1' if A else '0')
        term_binary_input += ('1' if B else '0')
        term_binary_input += ('1' if C else '0')
        term_binary_input += ('1' if D else '0')

        result_decimal = (i + 6) % 10
        output_bits = to_bcd(result_decimal)
        Y1, Y2, Y3, Y4 = output_bits[0], output_bits[1], output_bits[2], output_bits[3]

        print(f"{A} {B} {C} {D}\t\t"
              f"{Y1}  {Y2}  {Y3}  {Y4}")

        if Y1 == 1: sdnf_Y1.append(term_binary_input)
        if Y2 == 1: sdnf_Y2.append(term_binary_input)
        if Y3 == 1: sdnf_Y3.append(term_binary_input)
        if Y4 == 1: sdnf_Y4.append(term_binary_input)

    outputs_to_minimize = [
        ("Y1", sdnf_Y1), ("Y2", sdnf_Y2), ("Y3", sdnf_Y3), ("Y4", sdnf_Y4)
    ]

    for output_name, sdnf_terms_binary in outputs_to_minimize:
        print(f"\nСДНФ для {output_name}: ", end="")
        if not sdnf_terms_binary:
            print("0")
        else:
            sdnf_str_formatted = "|".join([f"({format_dnf_term(term, var_names)})" for term in sdnf_terms_binary])
            print(sdnf_str_formatted)

            terms_for_minimization = [Term(bin_term) for bin_term in sdnf_terms_binary]
            minimized_form = glue_terms(terms_for_minimization, var_names)

            print(f"Минимизированная форма {output_name}: ", end="")
            if not minimized_form:
                print("0")
            else:
                minimized_form_formatted = "|".join([f"({format_dnf_term(term.vars, var_names)})" for term in minimized_form])
                print(minimized_form_formatted)

def process_bcd_conversion(input_number: int):
    print(f"\n=== Обработка числа {input_number} ===")
    decimal_input = input_number % 10 if input_number >= 0 else 0
    result_decimal = (decimal_input + 6) % 10

    input_bits = to_bcd(decimal_input)
    output_bits = to_bcd(result_decimal)

    print(f"Входное число: {input_number} (используется: {decimal_input}, результат: {result_decimal})")
    print(f"Вход (Д8421): {input_bits[0]} {input_bits[1]} {input_bits[2]} {input_bits[3]}")
    print(f"Выход (Д8421+6): {output_bits[0]} {output_bits[1]} {output_bits[2]} {output_bits[3]} (десятичное: {result_decimal})")

if __name__ == "__main__":
    build_adder()
    print_bcd_converter_table_and_dnf()

    while True:
        try:
            input_number = int(input("\nВведите целое число (для выхода введите отрицательное число): "))
            if input_number < 0:
                break
            process_bcd_conversion(input_number)
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите целое число.")
