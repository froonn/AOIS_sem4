from lib import *

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
print(f'Binary: {mul_bits}, Decimal: {direct_to_dec(mul_bits)}, Overflow: {overflow}')

div_bin, div_dec = divide_direct(a, b)
print(f'\n{a} / {b} = {div_dec} in direct:')
print(f'Binary: {div_bin}, Decimal: {div_dec}')

a = float(input('\nEnter a fractional number: '))
b = float(input('Enter a fractional number: '))

ieee_sum, float_sum = add_ieee(a, b)
print(f'\n{a} + {b} = {a + b} in IEEE-754:')
print(f'Binary: {ieee_sum}, Decimal: {float_sum}')
