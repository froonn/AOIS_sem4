CHAR_SET = '0123456789_-' + \
           'abcdefghijklmnopqrstuvwxyz' + \
           'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + \
           'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' + \
           'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

BASE = len(CHAR_SET)

def get_char_value(char):
    try:
        return CHAR_SET.index(char)
    except ValueError:
        raise ValueError(f'Invalid character: \'{char}\'. Use only digits, Latin or Russian letters.')

def calculate_extended_hash(input_string, limit=8):
    if not isinstance(input_string, str):
        raise TypeError('Input must be a string.')

    hash_value = 0
    index = 0

    for char in input_string:
        char_value = get_char_value(char)
        hash_value += char_value * (BASE ** index)
        index += 1

    return hash_value % limit