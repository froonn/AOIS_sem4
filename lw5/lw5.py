import io
from functools import cmp_to_key

# Class to represent a term (implicant) in boolean minimization.
class Term:
    def __init__(self, vars_str):
        self.vars = vars_str # Binary representation of the term (e.g., "01-1")
        self.used = False    # Flag to indicate if the term has been used in a prime implicant
        # Set of original minterms covered by this implicant.
        # Initially, a term covers only itself.
        self.covered_terms = {vars_str}

# Checks if two terms can be "glued" (combined) according to Quine-McCluskey rules.
# They can be glued if they differ by exactly one bit.
def can_glue(t1: str, t2: str, var_count: int) -> bool:
    diff = 0  # Counter for differing bits
    for i in range(var_count):
        if t1[i] != t2[i]:
            diff += 1
        if diff > 1:
            return False  # More than one difference, cannot glue
    return diff == 1  # Must differ by exactly one bit

# Glues two terms that differ by exactly one bit.
# The differing bit is replaced with a '-'.
def glue(t1: str, t2: str) -> str:
    result = list(t1) # Convert to list for mutable string operations
    for i in range(len(t1)):
        if t1[i] != t2[i]:
            result[i] = '-'  # Replace differing bit with '-'
    return "".join(result) # Convert back to string

# Formats a binary term (e.g., "01-1") into a DNF (Disjunctive Normal Form) expression
# using variable names (e.g., "!Q3&Q2&V").
def format_dnf_term(term: str, var_names: list[str]) -> str:
    result = []
    for i, char in enumerate(term):
        if char == '-':
            continue # Skip don't-care positions
        if char == '0':
            result.append(f"!{var_names[i]}") # Negated variable
        elif char == '1':
            result.append(var_names[i])   # Non-negated variable
    return "&".join(result) if result else "1" # If empty (e.g., "----"), it represents '1'

# Implements the "gluing" (combining) stage of the Quine-McCluskey algorithm.
# It iteratively combines terms until no more terms can be combined.
def glue_terms(terms: list[Term], var_names: list[str]) -> list[Term]:
    print("Gluing stage:")
    var_count = len(var_names)
    glued = True # Flag to check if any terms were glued in an iteration

    while glued:
        glued = False
        new_terms_set = set() # Use a set to automatically handle unique terms
        used = [False] * len(terms) # Tracks if an original term was used in gluing

        # Iterate through all pairs of terms to find those that can be glued
        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                if can_glue(terms[i].vars, terms[j].vars, var_count):
                    glued_term_str = glue(terms[i].vars, terms[j].vars)
                    new_terms_set.add(glued_term_str) # Add the newly glued term
                    used[i] = used[j] = True          # Mark both original terms as used
                    glued = True                      # Indicate that gluing occurred

                    # Print the gluing operation
                    print(f"({format_dnf_term(terms[i].vars, var_names)}) | "
                          f"({format_dnf_term(terms[j].vars, var_names)}) => "
                          f"({format_dnf_term(glued_term_str, var_names)})")

        # Add any terms that were NOT used in gluing to the new set of terms.
        # These are prime implicants from the current stage.
        for i in range(len(terms)):
            if not used[i]:
                new_terms_set.add(terms[i].vars)

        # Prepare terms for the next iteration: clear the old terms and populate with new unique terms.
        terms = [Term(t) for t in new_terms_set]

    return terms # Return the final set of prime implicants

# Custom sort function for variable names: Q3, Q2, Q1, Q0, then V.
def _custom_var_sort_key(a, b):
    if a[0] == 'Q' and b[0] == 'Q':
        return int(b[1]) - int(a[1]) # Sort Q3 > Q2 > Q1 > Q0
    if a == "V":
        return 1 # V goes last
    if b == "V":
        return -1
    return (a > b) - (a < b) # Default alphabetical comparison for other cases

# Parses a boolean function in DNF (Disjunctive Normal Form) string format
# (e.g., "(!Q3&Q2)|(Q1&!V)") into a list of Term objects.
# It also extracts and sorts all unique string variable names found.
def parse_function(input_str: str, var_names: list[str]) -> list[Term]:
    terms = []
    var_names.clear() # Clear existing variable names to rebuild consistently
    unique_vars_set = set()

    # First pass: collect all unique string variable names from the entire input function
    temp_terms_str = input_str.split('|')
    for temp_term_str in temp_terms_str:
        temp_term_str = temp_term_str.replace(' ', '') # Remove spaces
        if not temp_term_str:
            continue

        pos = 0
        while pos < len(temp_term_str):
            # Skip '!' if present
            if temp_term_str[pos] == '!':
                pos += 1

            current_var_name = ""
            # Check for 'Q' variables (Q0, Q1, Q2, Q3)
            if pos + 1 < len(temp_term_str) and temp_term_str[pos] == 'Q' and temp_term_str[pos+1].isdigit():
                current_var_name = temp_term_str[pos:pos+2]
                pos += 2
            # Check for 'V' variable
            elif pos < len(temp_term_str) and temp_term_str[pos] == 'V':
                current_var_name = "V"
                pos += 1
            else:
                pos += 1 # Skip '&' or any other unrecognized character
                continue
            unique_vars_set.add(current_var_name)

            # Skip '&' if present
            if pos < len(temp_term_str) and temp_term_str[pos] == '&':
                pos += 1

    # Populate var_names from the set and sort them in a specific order: Q3, Q2, Q1, Q0, V
    var_names.extend(sorted(list(unique_vars_set), key=cmp_to_key(_custom_var_sort_key)))

    # Second pass: parse each term into its binary representation
    for term_str_from_ss in temp_terms_str:
        term_str_from_ss = term_str_from_ss.replace(' ', '') # Remove spaces
        if not term_str_from_ss:
            continue

        parsed_binary_term = ['-'] * len(var_names) # Initialize with '-' for all variables

        pos = 0
        while pos < len(term_str_from_ss):
            negated = False
            if term_str_from_ss[pos] == '!':
                negated = True
                pos += 1 # Move past '!'

            current_var_name = ""
            # Check for 'Q' variables (Q0, Q1, Q2, Q3)
            if pos + 1 < len(term_str_from_ss) and term_str_from_ss[pos] == 'Q' and temp_term_str[pos+1].isdigit():
                current_var_name = term_str_from_ss[pos:pos+2]
                pos += 2
            # Check for 'V' variable
            elif pos < len(term_str_from_ss) and term_str_from_ss[pos] == 'V':
                current_var_name = "V"
                pos += 1
            else:
                pos += 1 # Skip '&' or any other unrecognized character
                continue

            # Find the index of the current variable in the `var_names` list
            try:
                index = var_names.index(current_var_name)
                parsed_binary_term[index] = '0' if negated else '1'
            except ValueError:
                # Variable not found, which shouldn't happen if the first pass is correct
                pass

            # Skip '&' if present
            if pos < len(term_str_from_ss) and term_str_from_ss[pos] == '&':
                pos += 1

        terms.append(Term("".join(parsed_binary_term)))
    return terms

# Helper function to print the header row for truth tables.
def print_truth_table_header(arguments: list[str], col_width: int):
    header = ""
    for arg in arguments:
        header += f"{arg:<{col_width}}|"
    print(header)
    print("-" * (len(arguments) * (col_width + 1) - 1))

# Helper function to print a row in the truth table for the subtractor counter.
def print_truth_table_row(Q3: int, Q2: int, Q1: int, Q0: int, V: int,
                           Q3_next: int, Q2_next: int, Q1_next: int, Q0_next: int,
                           h3: int, h2: int, h1: int, h0: int, col_width: int):
    print(f"{Q3:<{col_width}}|"
          f"{Q2:<{col_width}}|"
          f"{Q1:<{col_width}}|"
          f"{Q0:<{col_width}}|"
          f"{V:<{col_width}}|"
          f"{Q3_next:<{col_width}}|"
          f"{Q2_next:<{col_width}}|"
          f"{Q1_next:<{col_width}}|"
          f"{Q0_next:<{col_width}}|"
          f"{h3:<{col_width}}|"
          f"{h2:<{col_width}}|"
          f"{h1:<{col_width}}|"
          f"{h0:<{col_width}}")

# Generates a DNF term string for the given state and input V.
def generate_sdnf_term(Q3: int, Q2: int, Q1: int, Q0: int, V: int) -> str:
    term_parts = []
    term_parts.append("Q3" if Q3 else "!Q3")
    term_parts.append("Q2" if Q2 else "!Q2")
    term_parts.append("Q1" if Q1 else "!Q1")
    term_parts.append("Q0" if Q0 else "!Q0")
    term_parts.append("V" if V else "!V")
    return "&".join(term_parts)

# Minimizes a boolean function represented by its SDNF terms.
def minimize_function(sdnf: list[str], h_index: int, var_names: list[str]):
    sdnf_str = "|".join([f"({term})" for term in sdnf])

    print(f"\nMinimization h{h_index}:")
    print(f"SDNF: {sdnf_str if sdnf_str else '0'}")

    if sdnf_str:
        # var_names for minimization are derived from the input variables
        var_names_h = list(var_names) # Use a copy of the provided var_names
        terms_h = parse_function(sdnf_str, var_names_h)
        minimized_h = glue_terms(terms_h, var_names_h)

        print("Minimized form in NOT, AND, OR basis: ", end="")
        minimized_terms_dnf = [format_dnf_term(term.vars, var_names_h) for term in minimized_h]
        print("|".join([f"({t})" for t in minimized_terms_dnf]))
    else:
        print("Minimized form: 0")

# Builds and displays the truth table and minimization for a 4-bit subtractor counter.
def print_subtractor_counter():
    print("Truth table of subtractor counter (variant 3)")
    # Argument names for the truth table header
    arguments = ["Q3", "Q2", "Q1", "Q0", "V", "Q3'", "Q2'", "Q1'", "Q0'", "h3", "h2", "h1", "h0"]
    col_width = 4 # Column width for table formatting

    print_truth_table_header(arguments, col_width)

    # Lists to store SDNF terms for each output function (h3, h2, h1, h0)
    sdnf_h3, sdnf_h2, sdnf_h1, sdnf_h0 = [], [], [], []

    # Loop through all 16 possible states (0 to 15)
    for state in range(15, -1, -1): # Iterate from 15 down to 0
        # Current state bits
        Q3 = (state >> 3) & 1
        Q2 = (state >> 2) & 1
        Q1 = (state >> 1) & 1
        Q0 = state & 1

        # Calculate the next state (decrement, with wrap-around from 0 to 15)
        next_state = 15 if state == 0 else state - 1
        # Next state bits
        Q3_next = (next_state >> 3) & 1
        Q2_next = (next_state >> 2) & 1
        Q1_next = (next_state >> 1) & 1
        Q0_next = next_state & 1

        # Input V is always 1 for this variant of the counter
        V = 1

        # Calculate the excitation functions (h_i) using XOR with next state
        # These represent the inputs required for flip-flops to transition from Q to Q_next.
        h3 = Q3 ^ Q3_next
        h2 = Q2 ^ Q2_next
        h1 = Q1 ^ Q1_next
        h0 = Q0 ^ Q0_next

        # Print the current row of the truth table
        print_truth_table_row(Q3, Q2, Q1, Q0, V, Q3_next, Q2_next, Q1_next, Q0_next, h3, h2, h1, h0, col_width)

        # Generate the current minterm string (e.g., "!Q3&!Q2&!Q1&!Q0&V")
        term = generate_sdnf_term(Q3, Q2, Q1, Q0, V)

        # Collect minterms where each h_i function is '1'
        if h3 == 1: sdnf_h3.append(term)
        if h2 == 1: sdnf_h2.append(term)
        if h1 == 1: sdnf_h1.append(term)
        if h0 == 1: sdnf_h0.append(term)

    # Define the variable names for minimization functions (inputs to h_i)
    var_names_for_minimization = ["Q3", "Q2", "Q1", "Q0", "V"]

    # Minimize each excitation function
    minimize_function(sdnf_h3, 3, var_names_for_minimization)
    minimize_function(sdnf_h2, 2, var_names_for_minimization)
    minimize_function(sdnf_h1, 1, var_names_for_minimization)
    minimize_function(sdnf_h0, 0, var_names_for_minimization)

if __name__ == "__main__":
    print_subtractor_counter()
