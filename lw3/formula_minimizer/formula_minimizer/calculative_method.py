from .minimizer_engine import *

def calculated_method_dnf(min_terms, labels):
    bit_size = len(labels)

    print("\n==== Оптимизация ДНФ (вычислительный метод) ====")
    core = calculate_core_terms(min_terms, bit_size, labels, True)
    critical = find_critical_terms(core, min_terms, bit_size, labels, True)
    optimized = remove_redundant_terms(critical, min_terms, bit_size)

    final_expr = " | ".join(f"({binary_to_expression(x, labels, True)})" for x in optimized)
    final_expr = " | ".join(labels) if final_expr.strip() == "1" else final_expr
    print("\nИТОГ (ДНФ): " + final_expr)
    return final_expr

def calculated_method_cnf(max_terms, labels):
    bit_size = len(labels)

    print("\n==== Оптимизация КНФ (вычислительный метод) ====")
    core = calculate_core_terms(max_terms, bit_size, labels, False)
    critical = find_critical_terms(core, max_terms, bit_size, labels, False)
    optimized = remove_redundant_terms(critical, max_terms, bit_size)
    result_terms = find_essential_implicants(optimized, labels, False)

    final_expr = " & ".join(f"({binary_to_expression(x, labels, False)})" for x in result_terms)
    print("\nИТОГ (КНФ): " + final_expr)
    return final_expr

