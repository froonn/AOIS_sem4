from .minimizer_engine import *


def tabular_method_dnf(terms, variable_names):
    num_vars = len(variable_names)

    print("\n==== Оптимизация ДНФ (комбинированный подход) ====")

    # Основной процесс обработки
    core_primes = process_with_table_method(terms, num_vars, variable_names, True)
    key_implicants = find_critical_terms(core_primes, terms, num_vars, variable_names, True)
    simplified_terms = remove_redundant_terms(key_implicants, terms, num_vars)

    # Формирование результата
    output_expressions = [f"({binary_to_expression(t, variable_names, True)})"
                          for t in simplified_terms]
    final_result = " | ".join(output_expressions)
    print(f"\nИтоговое выражение (ДНФ): {final_result}")
    return final_result


def tabular_method_cnf(terms, variable_names):
    num_vars = len(variable_names)

    print("\n==== Оптимизация КНФ (комбинированный подход) ====")

    # Вычислительный процесс
    core_primes = process_with_table_method(terms, num_vars, variable_names, False)
    key_implicants = find_critical_terms(core_primes, terms, num_vars, variable_names, False)
    simplified_terms = remove_redundant_terms(key_implicants, terms, num_vars)
    final_implicants = find_essential_implicants(simplified_terms, variable_names, False)

    # Сборка финального выражения
    cnf_components = [f"({binary_to_expression(f, variable_names, False)})"
                      for f in final_implicants]
    optimized_result = " & ".join(cnf_components)
    print(f"\nИтоговое выражение (КНФ): {optimized_result}")
    return optimized_result