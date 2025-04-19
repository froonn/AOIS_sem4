import unittest

from lib import *

class TestBinaryOperations(unittest.TestCase):

    def test_dec_to_bin_converts_positive_numbers_correctly(self):
        self.assertEqual(dec_to_bin(5, 4), '0101')
        self.assertEqual(dec_to_bin(10, 8), '00001010')

    def test_dec_to_bin_handles_zero_correctly(self):
        self.assertEqual(dec_to_bin(0, 4), '0000')
        self.assertEqual(dec_to_bin(0, 8), '00000000')

    def test_dec_to_bin_truncates_excess_bits(self):
        self.assertEqual(dec_to_bin(255, 8), '11111111')
        self.assertEqual(dec_to_bin(255, 4), '1111')

    def test_bin_to_dec_converts_binary_to_decimal(self):
        self.assertEqual(bin_to_dec('0101'), 5)
        self.assertEqual(bin_to_dec('00001010'), 10)

    def test_bin_to_dec_handles_empty_string(self):
        self.assertEqual(bin_to_dec(''), 0)

    def test_direct_code_encodes_positive_numbers_correctly(self):
        self.assertEqual(direct_code(5, 8), '00000101')
        self.assertEqual(direct_code(10, 8), '00001010')

    def test_direct_code_encodes_negative_numbers_correctly(self):
        self.assertEqual(direct_code(-5, 8), '10000101')
        self.assertEqual(direct_code(-10, 8), '10001010')

    def test_reverse_code_encodes_positive_numbers_correctly(self):
        self.assertEqual(reverse_code(5, 8), '00000101')
        self.assertEqual(reverse_code(10, 8), '00001010')

    def test_reverse_code_encodes_negative_numbers_correctly(self):
        self.assertEqual(reverse_code(-5, 8), '11111010')
        self.assertEqual(reverse_code(-10, 8), '11110101')

    def test_complement_code_encodes_positive_numbers_correctly(self):
        self.assertEqual(complement_code(5, 8), '00000101')
        self.assertEqual(complement_code(10, 8), '00001010')

    def test_complement_code_encodes_negative_numbers_correctly(self):
        self.assertEqual(complement_code(-5, 8), '11111011')
        self.assertEqual(complement_code(-10, 8), '11110110')

    def test_add_binary_adds_binary_numbers_correctly(self):
        self.assertEqual(add_binary('0101', '0011'), ('1000', 0))
        self.assertEqual(add_binary('1111', '0001'), ('10000', 1))

    def test_add_binary_handles_carry_correctly(self):
        self.assertEqual(add_binary('1111', '1111'), ('11110', 1))

    def test_complement_to_dec_converts_positive_complement_correctly(self):
        self.assertEqual(complement_to_dec('00000101'), 5)
        self.assertEqual(complement_to_dec('00001010'), 10)

    def test_complement_to_dec_converts_negative_complement_correctly(self):
        self.assertEqual(complement_to_dec('11111011'), -5)
        self.assertEqual(complement_to_dec('11110110'), -10)

    def test_add_complement_adds_numbers_correctly(self):
        self.assertEqual(add_complement(5, 3, 8), ('00001000', False))
        self.assertEqual(add_complement(-5, -3, 8), ('11111000', False))

    def test_add_complement_detects_overflow(self):
        self.assertEqual(add_complement(127, 1, 8), ('10000000', True))
        self.assertEqual(add_complement(-128, -1, 8), ('01111111', True))

    def test_subtract_complement_subtracts_numbers_correctly(self):
        self.assertEqual(subtract_complement(5, 3, 8), ('00000010', False))
        self.assertEqual(subtract_complement(-5, -3, 8), ('11111110', False))

    def test_binary_compare_compares_binary_strings_correctly(self):
        self.assertEqual(binary_compare('0101', '0101'), 0)
        self.assertEqual(binary_compare('0101', '0011'), 1)
        self.assertEqual(binary_compare('0011', '0101'), -1)

    def test_binary_multiply_multiplies_binary_numbers_correctly(self):
        self.assertEqual(binary_multiply('0101', '0011'), '01111')
        self.assertEqual(binary_multiply('1111', '0001'), '1111')

    def test_binary_divide_divides_binary_numbers_correctly(self):
        self.assertEqual(binary_divide('1010', '0010', 0), '101')
        self.assertEqual(binary_divide('1010', '0010', 2), '101.00')

    def test_binary_divide_raises_error_on_division_by_zero(self):
        with self.assertRaises(ValueError):
            binary_divide('1010', '0000', 0)

    def test_divide_direct_handles_division_with_precision(self):
        result_bin, result_dec = divide_direct(10, 3, bits=16, precision=3)
        self.assertEqual(result_bin, '11.010')
        self.assertAlmostEqual(result_dec, 3.25, places=3)

    def test_divide_direct_raises_error_on_division_by_zero(self):
        with self.assertRaises(ValueError):
            divide_direct(10, 0, bits=16, precision=5)

    def test_multiply_direct_handles_mixed_sign_numbers(self):
        result_bin, overflow = multiply_direct(-5, -3, bits=16)
        self.assertEqual(result_bin, '0000000000001111')
        self.assertFalse(overflow)

    def test_multiply_direct_detects_overflow(self):
        result_bin, overflow = multiply_direct(32767, 2, bits=16)
        self.assertEqual(result_bin, '0111111111111110')
        self.assertTrue(overflow)

    def test_multiply_direct_handles_zero(self):
        result_bin, overflow = multiply_direct(0, 5, bits=16)
        self.assertEqual(result_bin, '0000000000000000')
        self.assertFalse(overflow)

    def test_divide_direct_handles_large_numbers(self):
        result_bin, result_dec = divide_direct(32767, 3, bits=16, precision=5)
        self.assertEqual(result_bin, '10101010101010.01010')
        self.assertAlmostEqual(result_dec, 10922.3125, places=5)

    def test_float_to_ieee_converts_zero_correctly(self):
        self.assertEqual(float_to_ieee(0.0), '00000000000000000000000000000000')

    def test_float_to_ieee_converts_positive_numbers_correctly(self):
        self.assertEqual(float_to_ieee(1.0), '00111111100000000000000000000000')
        self.assertEqual(float_to_ieee(2.0), '01000000000000000000000000000000')

    def test_float_to_ieee_converts_negative_numbers_correctly(self):
        self.assertEqual(float_to_ieee(-1.0), '10111111100000000000000000000000')
        self.assertEqual(float_to_ieee(-2.0), '11000000000000000000000000000000')

    def test_add_ieee_adds_floats_correctly(self):
        ieee_sum, float_sum = add_ieee(1.0, 2.0)
        self.assertEqual(ieee_sum, '01000000010000000000000000000000')
        self.assertAlmostEqual(float_sum, 3.0, places=5)

if __name__ == '__main__':
    unittest.main()