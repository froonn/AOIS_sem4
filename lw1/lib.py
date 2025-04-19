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

def binary_compare(a, b):
    max_len = max(len(a), len(b))
    a_filled = a.zfill(max_len)
    b_filled = b.zfill(max_len)
    if a_filled == b_filled:
        return 0
    for i in range(max_len):
        if a_filled[i] != b_filled[i]:
            return 1 if a_filled[i] == '1' else -1
    return 0

def binary_add(a, b):
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
    return ''.join(reversed(result))

def binary_subtract(a, b):
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    result = []
    borrow = 0
    for i in reversed(range(max_len)):
        a_val = int(a[i]) - borrow
        b_val = int(b[i])
        if a_val < b_val:
            a_val += 2
            borrow = 1
        else:
            borrow = 0
        result.append(str(a_val - b_val))
    return ''.join(reversed(result)).lstrip('0') or '0'

def binary_multiply(a_bin, b_bin):
    result = '0'
    for i in reversed(range(len(b_bin))):
        if b_bin[i] == '1':
            temp = a_bin + '0' * (len(b_bin) - i - 1)
            result = binary_add(result, temp)
    return result

def binary_divide(a_bin, b_bin, precision):
    if all(c == '0' for c in b_bin):
        raise ValueError('Division by zero')

    quotient = ''
    current = ''
    divisor = b_bin.lstrip('0') or '0'

    for bit in a_bin:
        current += bit
        current = current.lstrip('0') or '0'
        if binary_compare(current, divisor) >= 0:
            quotient += '1'
            current = binary_subtract(current, divisor)
            current = current.lstrip('0') or '0'
        else:
            quotient += '0'

    quotient = quotient.lstrip('0') or '0'
    if '.' in quotient:
        quotient = quotient.rstrip('0').rstrip('.')

    if precision > 0:
        quotient += '.' if '.' not in quotient else ''
        for _ in range(precision):
            current += '0'
            if binary_compare(current, divisor) >= 0:
                quotient += '1'
                current = binary_subtract(current, divisor)
                current = current.lstrip('0') or '0'
            else:
                quotient += '0'

    return quotient if quotient != '' else '0'

def direct_to_dec(binary_str):
    if not binary_str:
        return 0
    sign_bit = binary_str[0] if binary_str[0] in ('0', '1') else '0'
    magnitude = binary_str[1:] if len(binary_str) > 1 else '0'
    dec = bin_to_dec(magnitude) if magnitude else 0
    return -dec if sign_bit == '1' else dec

def multiply_direct(a_dec, b_dec, bits=16):
    sign = 0 if (a_dec >= 0) == (b_dec >= 0) else 1
    a_abs = abs(a_dec)
    b_abs = abs(b_dec)

    a_bin = dec_to_bin(a_abs, 15)
    b_bin = dec_to_bin(b_abs, 15)

    product_bin = binary_multiply(a_bin, b_bin)
    product_stripped = product_bin.lstrip('0') or '0'
    overflow = len(product_stripped) > 15
    product_bin = product_stripped[-15:] if overflow else product_stripped.zfill(15)
    product_bin = product_bin.zfill(15)

    signed_bin = ('1' if sign else '0') + product_bin
    return signed_bin, overflow

def divide_direct(a_dec, b_dec, bits=16, precision=5):
    if b_dec == 0:
        raise ValueError('Division by zero')
    sign = 0 if (a_dec >= 0) == (b_dec >= 0) else 1
    a_abs = abs(a_dec)
    b_abs = abs(b_dec)

    a_bin = dec_to_bin(a_abs, 15)
    b_bin = dec_to_bin(b_abs, 15)

    result_bin = binary_divide(a_bin, b_bin, precision)
    dec = bin_to_dec(result_bin.split('.')[0]) if '.' in result_bin else bin_to_dec(result_bin)
    if '.' in result_bin:
        frac_part = result_bin.split('.')[1]
        dec += sum(int(bit) * 2 ** -(i+1) for i, bit in enumerate(frac_part))
    dec = -dec if sign else dec

    return result_bin, round(dec, 5)

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
        exponent = int(ieee[1:9], 2)
        mantissa_bits = ieee[9:]
        mantissa = 1.0 if exponent != 0 else 0.0
        for i, bit in enumerate(mantissa_bits):
            mantissa += int(bit) * 2**(-i-1)
        return sign, exponent, mantissa, mantissa_bits

    def align_mantissas(sign1, exp1, mant1, sign2, exp2, mant2):
        if exp1 < exp2:
            return align_mantissas(sign2, exp2, mant2, sign1, exp1, mant1)

        diff = exp1 - exp2
        if diff > 0:
            mant2_adjusted = mant2 / (2**diff)
            exp2_adjusted = exp1
        else:
            mant2_adjusted = mant2
            exp2_adjusted = exp2

        return (sign1, exp1, mant1, sign2, exp2_adjusted, mant2_adjusted)

    def pack_ieee(sign, exponent, mantissa):
        if mantissa == 0:
            return '0' * 32

        original_sign = sign
        mantissa = abs(mantissa)

        while mantissa >= 2.0:
            mantissa /= 2
            exponent += 1
        while mantissa < 1.0 and exponent > 0:
            mantissa *= 2
            exponent -= 1

        if exponent <= 0:
            exponent = 0
            mantissa /= 2**(-exponent + 1)

        mantissa -= 1.0
        mantissa_bits = []
        for _ in range(23):
            mantissa *= 2
            if mantissa >= 1.0:
                mantissa_bits.append('1')
                mantissa -= 1.0
            else:
                mantissa_bits.append('0')

        exponent = max(0, min(exponent, 255))
        return f"{original_sign}{exponent:08b}{''.join(mantissa_bits)}"

    a_ieee = float_to_ieee(a_dec)
    b_ieee = float_to_ieee(b_dec)

    sign_a, exp_a, mant_a, _ = parse_ieee(a_ieee)
    sign_b, exp_b, mant_b, _ = parse_ieee(b_ieee)

    sign1, exp, mant1, sign2, exp, mant2 = align_mantissas(
        sign_a, exp_a, mant_a,
        sign_b, exp_b, mant_b
    )

    mant1 = mant1 if sign1 == '0' else -mant1
    mant2 = mant2 if sign2 == '0' else -mant2

    result_mant = mant1 + mant2
    result_sign = '0' if result_mant >= 0 else '1'

    result_ieee = pack_ieee(result_sign, exp, abs(result_mant))
    decoded = (-1 if result_sign == '1' else 1) * abs(result_mant) * (2**(exp - 127))

    return result_ieee, decoded

