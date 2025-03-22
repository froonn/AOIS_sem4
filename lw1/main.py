def to_direct_binary(a: int, bits=16) -> str:
    result = ['0' for i in range(bits)]

    if a < 0:
        result[-1] = '1'
        a *= -1

    for i in range(bits):
        result[i] = str(a % 2)
        a = a // 2
        if a == 0:
            break

    return ''.join(result[::-1])


def to_reverse_binary(a: int, bits=16) -> str:
    if a >= 0:
        return to_direct_binary(a, bits)
    else:
        return '1' + to_direct_binary(a, bits)[1:].translate(str.maketrans('01', '10'))


def to_additional_binary(a: int, bits=16) -> str:
    if a >= 0:
        return to_direct_binary(a, bits)
    else:
        return '1' + to_direct_binary(abs(a) - 1, bits)[1:].translate(str.maketrans('01', '10'))


def add_binary(a: str, b: str) -> str:
    max_len = max(len(a), len(b))
    result = ''
    carry = 0
    a = a[0] + '0' * (max_len - len(a)) + a[1:]
    b = b[0] + '0' * (max_len - len(b)) + b[1:]
    for i in range(max_len - 1, -1, -1):
        if a[i] == '0' and b[i] == '0' and carry == 0:
            result = '0' + result
        elif a[i] == '0' and b[i] == '0' and carry == 1:
            result = '1' + result
            carry = 0
        elif a[i] == '0' and b[i] == '1' and carry == 0:
            result = '1' + result
        elif a[i] == '0' and b[i] == '1' and carry == 1:
            result = '0' + result
        elif a[i] == '1' and b[i] == '0' and carry == 0:
            result = '1' + result
        elif a[i] == '1' and b[i] == '0' and carry == 1:
            result = '0' + result
        elif a[i] == '1' and b[i] == '1' and carry == 0:
            result = '0' + result
            carry = 1
        elif a[i] == '1' and b[i] == '1' and carry == 1:
            result = '1' + result
            carry = 1
        else:
            raise Exception
    return result


def sub_additional_binary(a: str, b: str) -> str:
    opposite_b = b.translate(str.maketrans('01', '10'))
    return add_binary(add_binary(a, opposite_b), to_additional_binary(1))

def sub_direct_binary(a: str, b: str) -> str:
    sign_a = a[0]
    sign_b = b[0]
    module_a = a[1:]
    module_b = b[1:]

    if sign_a == sign_b:
        if ge_binary(module_a, module_b):
            result_module = bin(int(module_a, 2) - int(module_b, 2))[2:].zfill(len(module_a))
            return sign_a + result_module
        else:
            result_module = bin(int(module_b, 2) - int(module_a, 2))[2:].zfill(len(module_b))
            return str(int(not int(sign_a))) + result_module
    else:
        result_module = bin(int(module_a, 2) + int(module_b, 2))[2:].zfill(max(len(module_a), len(module_b)))
        return sign_a + result_module


def ge_binary(a: str, b: str) -> bool:
    max_len = max(len(a), len(b))
    a = '0' * (max_len - len(a)) + a
    b = '0' * (max_len - len(b)) + b
    for i in range(max_len):
        if a[i] == '0' and b[i] == '1':
            return True
        elif a[i] == '1' and b[i] == '0':
            return False
    return True


def div_direct_binary(a: str, b: str) -> str:
    if '1' not in b[1:]:
        raise ZeroDivisionError
    max_len = max(len(a), len(b))
    result = list('0' * max_len)
    if '1' not in a:
        return ''.join(result)

    index_a = 1
    index_result = 0
    tmp = ''
    while True:
        tmp += a[index_a]
        if ge_binary(tmp, b[1:]):
            result[index_result] = '1'
            tmp = sub_direct_binary(tmp, b[1:])
        else:
            result[index_result] = '0'

        index_a += 1
        index_result += 1

    return str(int(a[0] != b[0])) + ''.join(result)

a = -25
b = 8
print(to_additional_binary(a))
print(to_additional_binary(b))

print(sub_additional_binary(to_additional_binary(a), to_additional_binary(b)))
print(to_additional_binary(a - b))
print(to_additional_binary(a - b) == sub_additional_binary(to_additional_binary(a), to_additional_binary(b)))
