import io
from functools import cmp_to_key


class BooleanMinTerm:
    def __init__(self, binary_str: str):
        self.binary_representation = binary_str
        self.is_processed = False
        self.original_minterms_covered = {binary_str}


def can_combine_terms(term1_binary: str, term2_binary: str, num_variables: int) -> bool:
    bit_differences = 0
    for i in range(num_variables):
        if term1_binary[i] != term2_binary[i]:
            bit_differences += 1
        if bit_differences > 1:
            return False
    return bit_differences == 1


def combine_terms(term1_binary: str, term2_binary: str) -> str:
    combined_representation = list(term1_binary)
    for i in range(len(term1_binary)):
        if term1_binary[i] != term2_binary[i]:
            combined_representation[i] = '-'
    return "".join(combined_representation)


def format_logical_expression(binary_term: str, variable_names: list[str]) -> str:
    expression_literals = []
    for i, bit_val in enumerate(binary_term):
        if bit_val == '-':
            continue
        if bit_val == '0':
            expression_literals.append(f"!{variable_names[i]}")
        elif bit_val == '1':
            expression_literals.append(variable_names[i])
    return "&".join(expression_literals) if expression_literals else "1"


def minimize_terms_quine_mccluskey(initial_terms: list[BooleanMinTerm], variable_names: list[str]) -> list[
    BooleanMinTerm]:
    print("\n--- Этап объединения импликантов ---")
    num_variables = len(variable_names)

    current_terms_stage = initial_terms

    found_new_combinations = True
    while found_new_combinations:
        found_new_combinations = False
        next_stage_implicants = set()

        term_used_flags = [False] * len(current_terms_stage)

        for i in range(len(current_terms_stage)):
            for j in range(i + 1, len(current_terms_stage)):
                term1 = current_terms_stage[i]
                term2 = current_terms_stage[j]

                if can_combine_terms(term1.binary_representation, term2.binary_representation, num_variables):
                    combined_binary_str = combine_terms(term1.binary_representation, term2.binary_representation)

                    new_implicant = BooleanMinTerm(combined_binary_str)
                    new_implicant.original_minterms_covered.update(term1.original_minterms_covered)
                    new_implicant.original_minterms_covered.update(term2.original_minterms_covered)

                    next_stage_implicants.add(new_implicant.binary_representation)

                    term_used_flags[i] = True
                    term_used_flags[j] = True
                    found_new_combinations = True

                    print(f"Объединены ({format_logical_expression(term1.binary_representation, variable_names)}) "
                          f"и ({format_logical_expression(term2.binary_representation, variable_names)}) "
                          f"для образования ({format_logical_expression(combined_binary_str, variable_names)})")

        for i in range(len(current_terms_stage)):
            if not term_used_flags[i]:
                next_stage_implicants.add(current_terms_stage[i].binary_representation)

        current_terms_stage = [BooleanMinTerm(t_str) for t_str in next_stage_implicants]

    return current_terms_stage


def _sort_alphanumeric_characters(char_a, char_b):
    return (char_a > char_b) - (char_a < char_b)


def parse_boolean_function_string(function_string: str, variable_names_list: list[str]) -> list[BooleanMinTerm]:
    function_terms = []
    variable_names_list.clear()
    unique_variables_found = set()

    raw_term_strings = function_string.split('|')

    for current_raw_term in raw_term_strings:
        cleaned_term = current_raw_term.replace(' ', '')
        if not cleaned_term:
            continue
        for char_in_term in cleaned_term:
            if char_in_term.isalpha():
                unique_variables_found.add(char_in_term)

    variable_names_list.extend(sorted(list(unique_variables_found), key=cmp_to_key(_sort_alphanumeric_characters)))

    for current_raw_term in raw_term_strings:
        cleaned_term = current_raw_term.replace(' ', '')
        if not cleaned_term:
            continue

        parsed_binary_rep = ['-'] * len(variable_names_list)

        position_in_term = 0
        while position_in_term < len(cleaned_term):
            variable_char = ''
            literal_value = ''

            if cleaned_term[position_in_term] == '!':
                variable_char = cleaned_term[position_in_term + 1]
                literal_value = '0'
                position_in_term += 2
            elif cleaned_term[position_in_term].isalpha():
                variable_char = cleaned_term[position_in_term]
                literal_value = '1'
                position_in_term += 1
            else:
                position_in_term += 1
                continue

            try:
                variable_index = variable_names_list.index(variable_char)
                parsed_binary_rep[variable_index] = literal_value
            except ValueError:
                pass

        new_minterm = BooleanMinTerm("".join(parsed_binary_rep))
        function_terms.append(new_minterm)
    return function_terms


def simulate_full_adder():
    print("\n=== Одноразрядный полный двоичный сумматор (3 входа) ===")
    adder_variable_names = ['A', 'B', 'C_in']
    sum_sdnf_terms, carry_out_sdnf_terms = [], []

    print("\nТаблица истинности для полного сумматора:")
    print("A B C_in | Сумма ВыходПереноса")
    print("---------+---------------")

    for input_A in range(2):
        for input_B in range(2):
            for input_C_in in range(2):
                binary_sum = input_A + input_B + input_C_in
                sum_output = binary_sum % 2
                carry_out = binary_sum // 2

                print(f"{input_A} {input_B} {input_C_in}    | {sum_output}    {carry_out}")

                current_binary_minterm = ""
                current_binary_minterm += ('1' if input_A else '0')
                current_binary_minterm += ('1' if input_B else '0')
                current_binary_minterm += ('1' if input_C_in else '0')

                if sum_output == 1:
                    sum_sdnf_terms.append(current_binary_minterm)
                if carry_out == 1:
                    carry_out_sdnf_terms.append(current_binary_minterm)

    sum_sdnf_str = "|".join([f"({format_logical_expression(term, adder_variable_names)})" for term in sum_sdnf_terms])
    print(f"\nСовершенная дизъюнктивная нормальная форма (СДНФ) для суммы (S): {sum_sdnf_str}")

    initial_sum_terms = [BooleanMinTerm(bin_term) for bin_term in sum_sdnf_terms]
    minimized_sum_form = minimize_terms_quine_mccluskey(initial_sum_terms, adder_variable_names)

    print("\nМинимизированное выражение для суммы (S): ", end="")
    formatted_minimized_sum = [f"({format_logical_expression(term.binary_representation, adder_variable_names)})" for
                               term in minimized_sum_form]
    print("|".join(formatted_minimized_sum))

    carry_out_sdnf_str = "|".join(
        [f"({format_logical_expression(term, adder_variable_names)})" for term in carry_out_sdnf_terms])
    print(f"\nСовершенная дизъюнктивная нормальная форма (СДНФ) для выходного переноса (C_out): {carry_out_sdnf_str}")

    initial_carry_out_terms = [BooleanMinTerm(bin_term) for bin_term in carry_out_sdnf_terms]
    minimized_carry_out_form = minimize_terms_quine_mccluskey(initial_carry_out_terms, adder_variable_names)

    print("\nМинимизированное выражение для выходного переноса (C_out): ", end="")
    formatted_minimized_carry_out = [f"({format_logical_expression(term.binary_representation, adder_variable_names)})"
                                     for term in minimized_carry_out_form]
    print("|".join(formatted_minimized_carry_out))
    print("")


def decimal_to_binary_coded_decimal(decimal_digit: int) -> list[int]:
    normalized_decimal = decimal_digit % 10
    bcd_output = [0] * 4

    bcd_output[0] = (normalized_decimal >> 3) & 1
    bcd_output[1] = (normalized_decimal >> 2) & 1
    bcd_output[2] = (normalized_decimal >> 1) & 1
    bcd_output[3] = normalized_decimal & 1
    return bcd_output


def generate_bcd_plus_six_conversion():
    print("\n=== Преобразователь BCD (8421) в BCD+6 ===")
    bcd_variable_names = ['D_input_A', 'D_input_B', 'D_input_C', 'D_input_D']

    sdnf_output_Y1, sdnf_output_Y2, sdnf_output_Y3, sdnf_output_Y4 = [], [], [], []

    print("\nВход BCD (D8421)\tВыход BCD+6 (D8421)")
    print("A B C D\t\tY1 Y2 Y3 Y4")
    print("-----------------------------------")

    for i in range(10):
        input_bcd_bits = decimal_to_binary_coded_decimal(i)

        D_input_A, D_input_B, D_input_C, D_input_D = input_bcd_bits[0], input_bcd_bits[1], input_bcd_bits[2], \
        input_bcd_bits[3]

        current_binary_input_term = ""
        current_binary_input_term += ('1' if D_input_A else '0')
        current_binary_input_term += ('1' if D_input_B else '0')
        current_binary_input_term += ('1' if D_input_C else '0')
        current_binary_input_term += ('1' if D_input_D else '0')

        resulting_decimal_value = (i + 6) % 10
        output_bcd_bits = decimal_to_binary_coded_decimal(resulting_decimal_value)

        output_Y1, output_Y2, output_Y3, output_Y4 = output_bcd_bits[0], output_bcd_bits[1], output_bcd_bits[2], \
        output_bcd_bits[3]

        print(f"{D_input_A} {D_input_B} {D_input_C} {D_input_D}\t\t"
              f"{output_Y1}  {output_Y2}  {output_Y3}  {output_Y4}")

        if output_Y1 == 1: sdnf_output_Y1.append(current_binary_input_term)
        if output_Y2 == 1: sdnf_output_Y2.append(current_binary_input_term)
        if output_Y3 == 1: sdnf_output_Y3.append(current_binary_input_term)
        if output_Y4 == 1: sdnf_output_Y4.append(current_binary_input_term)

    output_functions_to_minimize = [
        ("Y1", sdnf_output_Y1),
        ("Y2", sdnf_output_Y2),
        ("Y3", sdnf_output_Y3),
        ("Y4", sdnf_output_Y4)
    ]

    for function_name, sdnf_binary_terms in output_functions_to_minimize:
        print(f"\nСДНФ для {function_name}: ", end="")
        if not sdnf_binary_terms:
            print("0")
        else:
            formatted_sdnf_string = "|".join(
                [f"({format_logical_expression(term, bcd_variable_names)})" for term in sdnf_binary_terms])
            print(formatted_sdnf_string)

            initial_terms_for_minimization = [BooleanMinTerm(bin_term) for bin_term in sdnf_binary_terms]
            minimized_expression = minimize_terms_quine_mccluskey(initial_terms_for_minimization, bcd_variable_names)

            print(f"\nМинимизированное выражение для {function_name}: ", end="")
            if not minimized_expression:
                print("0")
            else:
                formatted_minimized_expression = "|".join(
                    [f"({format_logical_expression(term.binary_representation, bcd_variable_names)})" for term in
                     minimized_expression])
                print(formatted_minimized_expression)


def calculate_bcd_plus_six_for_input(input_value: int):
    print(f"\n--- Обработка входного числа: {input_value} ---")
    decimal_input_digit = input_value % 10 if input_value >= 0 else 0

    resulting_decimal_digit = (decimal_input_digit + 6) % 10

    input_bcd_representation = decimal_to_binary_coded_decimal(decimal_input_digit)
    output_bcd_representation = decimal_to_binary_coded_decimal(resulting_decimal_digit)

    print(
        f"Входное десятичное: {input_value} (Используется: {decimal_input_digit}, Результат: {resulting_decimal_digit})")
    print(f"Вход (BCD 8421): {' '.join(map(str, input_bcd_representation))}")
    print(
        f"Выход (BCD 8421+6): {' '.join(map(str, output_bcd_representation))} (Десятичное: {resulting_decimal_digit})")


if __name__ == "__main__":
    simulate_full_adder()

    generate_bcd_plus_six_conversion()

    while True:
        try:
            user_input_number = int(input("\nВведите целое число (для выхода введите отрицательное число): "))
            if user_input_number < 0:
                print("Выход из программы. До свидания!")
                break
            calculate_bcd_plus_six_for_input(user_input_number)
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите целое число.")
