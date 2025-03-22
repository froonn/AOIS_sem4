def to_direct_binary(a: int, bits = 8) -> str:
    result = ['0' for i in range(bits)]

    if a < 0:
        result[-1] = '1'
        a *= -1

    for i in range(5):
        result[i] = str(a % 2)
        a = a // 2
        if a == 0:
            break

    return ''.join(result[::-1])

print(to_direct_binary(40))
