def dec_to_bin(n, bits):
    if bits == 0:
        return ''
    if n == 0:
        return '0' * bits
    binary = ''
    count = 0
    while n > 0 and count < bits:
        binary = str(n % 2) + binary
        n = n // 2
        count += 1
    while len(binary) < bits:
        binary = '0' + binary
    return binary[-bits:]

def bin_to_dec(bin_str):
    dec = 0
    for bit in bin_str:
        dec = dec * 2 + int(bit)
    return dec

def direct_code(n, bits):
    if n >= 0:
        return '0' + dec_to_bin(n, bits-1)
    else:
        return '1' + dec_to_bin(abs(n), bits-1)

def reverse_code(n, bits):
    direct = direct_code(n, bits)
    if n >= 0:
        return direct
    sign = direct[0]
    magnitude = direct[1:]
    inverted = ''.join(['1' if b == '0' else '0' for b in magnitude])
    return sign + inverted

def complement_code(n, bits):
    reverse = reverse_code(n, bits)
    if n >= 0:
        return reverse
    magnitude = reverse[1:]
    carry = 1
    result = []
    for bit in reversed(magnitude):
        if carry == 0:
            result.append(bit)
        else:
            if bit == '0':
                result.append('1')
                carry = 0
            else:
                result.append('0')
    if carry == 1:
        result.append('1')
    else:
        result.append('0')
    result = ''.join(reversed(result))
    return reverse[0] + result[-len(magnitude):]

def add_binary(a, b):
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    carry = 0
    result = []
    for i in reversed(range(max_len)):
        s = int(a[i]) + int(b[i]) + carry
        result.append(str(s % 2))
        carry = s // 2
    if carry:
        result.append('1')
    return ''.join(reversed(result)), carry

def complement_to_dec(bin_str):
    if bin_str[0] == '0':
        return bin_to_dec(bin_str)
    else:
        magnitude = bin_str[1:]
        inverted = ''.join(['1' if b == '0' else '0' for b in magnitude])
        sum_, carry = add_binary(inverted, '1')
        return -bin_to_dec(sum_)

def add_complement(a_dec, b_dec, bits=16):
    a_bin = complement_code(a_dec, bits)
    b_bin = complement_code(b_dec, bits)
    sum_bits, carry = add_binary(a_bin, b_bin)
    sum_bits = sum_bits[-bits:]
    sign_a = a_bin[0]
    sign_b = b_bin[0]
    sign_sum = sum_bits[0]
    overflow = (sign_a == sign_b) and (sign_sum != sign_a)
    return sum_bits, overflow

def subtract_complement(a_dec, b_dec, bits=16):
    return add_complement(a_dec, -b_dec, bits)

def multiply_direct(a_dec, b_dec, bits=16):
    sign = 0 if (a_dec >= 0) == (b_dec >= 0) else 1
    a_abs = abs(a_dec)
    b_abs = abs(b_dec)
    a_bin = dec_to_bin(a_abs, 15)
    b_bin = dec_to_bin(b_abs, 15)
    product = bin_to_dec(a_bin) * bin_to_dec(b_bin)
    product_bin = dec_to_bin(product, 15)
    return ('0' if sign == 0 else '1') + product_bin

def divide_direct(a_dec, b_dec, bits=16, precision=5):
    if b_dec == 0:
        raise ValueError('Division by zero')
    sign = 0 if (a_dec >= 0) == (b_dec >= 0) else 1
    a_abs = abs(a_dec)
    b_abs = abs(b_dec)
    int_part = a_abs // b_abs
    remainder = a_abs % b_abs
    int_bin = dec_to_bin(int_part, 15)
    frac_bin = ''
    for _ in range(precision):
        remainder *= 2
        bit = remainder // b_abs
        frac_bin += str(bit)
        remainder %= b_abs
    int_bin = int_bin.zfill(15)
    binary = f'{int_bin}.{frac_bin}'
    dec = int_part
    for i in range(len(frac_bin)):
        dec += int(frac_bin[i]) * 2**-(i+1)
    if sign:
        dec = -dec
    # direct = direct_code(int_part, bits) if dec == int_part else f'Sign: {sign}, {binary}'
    return binary, round(dec, 5)

def float_to_ieee(f):
    if f == 0:
        return '0' * 32

    sign = '1' if f < 0 else '0'
    f = abs(f)

    exp = 0
    if f >= 2.0:
        while f >= 2.0:
            f /= 2
            exp += 1
    elif f < 1.0:
        while f < 1.0:
            f *= 2
            exp -= 1
    exp += 127

    f -= 1.0
    mantissa = []
    for _ in range(23):
        f *= 2
        if f >= 1.0:
            mantissa.append('1')
            f -= 1.0
        else:
            mantissa.append('0')

    return f"{sign}{exp:08b}{''.join(mantissa)}"

def add_ieee(a_dec, b_dec):
    def parse_ieee(ieee):
        sign = ieee[0]
        exp = int(ieee[1:9], 2) - 127
        mantissa = 1.0 + sum(int(ieee[9+i]) * 2**(-i-1) for i in range(23))
        return (-1 if sign == '1' else 1) * mantissa * 2**exp

    a_ieee = float_to_ieee(a_dec)
    b_ieee = float_to_ieee(b_dec)

    result = parse_ieee(a_ieee) + parse_ieee(b_ieee)

    return float_to_ieee(result), result

def main():

    bits = 16

    a = int(input('Enter a number: '))
    b = int(input('Enter a number: '))

    print(f'\nDecimal: {a}')
    print(f'Direct: {direct_code(a, bits)}')
    print(f'Reverse: {reverse_code(a, bits)}')
    print(f'Complement: {complement_code(a, bits)}')

    print(f'\nDecimal: {b}')
    print(f'Direct: {direct_code(b, bits)}')
    print(f'Reverse: {reverse_code(b, bits)}')
    print(f'Complement: {complement_code(b, bits)}')

    sum_bits, overflow = add_complement(a, b)
    print(f'\n{a} + {b} = {a + b} in complement:')
    print(f'Binary: {sum_bits}, Decimal: {complement_to_dec(sum_bits)}, Overflow: {overflow}')

    sub_bits, overflow = subtract_complement(a, b)
    print(f'\n{a} - {b} = {a - b} in complement:')
    print(f'Binary: {sub_bits}, Decimal: {complement_to_dec(sub_bits)}, Overflow: {overflow}')

    mul_bits, overflow = multiply_direct(a, b)
    print(f'\n{a} * {b} = {a * b} in complement:')
    print(f'Binary: {mul_bits}, Decimal: {complement_to_dec(mul_bits)}, Overflow: {overflow}')

    div_bin, div_dec = divide_direct(a, b)
    print(f'\n{a} / {b} = {div_dec} in direct:')
    print(f'Binary: {div_bin}, Decimal: {div_dec}')

    a = float(input('Enter a fractional number: '))
    b = float(input('Enter a fractional number: '))

    ieee_sum, float_sum = add_ieee(a, b)
    print(f'\n{a} + {b} = {a + b} in IEEE-754:')
    print(f'Binary: {ieee_sum}, Decimal: {float_sum}')

if __name__ == '__main__':
    main()