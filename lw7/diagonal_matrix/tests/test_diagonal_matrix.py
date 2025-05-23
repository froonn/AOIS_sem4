import unittest
from diagonal_matrix.diagonal_matrix.daigonal_matrix import DiagonalMatrix


class TestDiagonalMatrix(unittest.TestCase):

    def setUp(self):
        self.matrix = DiagonalMatrix(size=16)
        self.matrix.init_from_list([
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])


    def test_init(self):
        matrix = DiagonalMatrix()
        self.assertEqual(matrix._size, 16)
        self.assertEqual(matrix._matrix, [[False] * 16 for _ in range(16)])

        matrix_custom_size = DiagonalMatrix(size=8)
        self.assertEqual(matrix_custom_size._size, 8)
        self.assertEqual(matrix_custom_size._matrix, [[False] * 8 for _ in range(8)])

    def test_init_from_list(self):
        matrix = DiagonalMatrix(size=2)
        data_valid = [[0, 1], [1, 0]]
        matrix.init_from_list(data_valid)
        self.assertEqual(matrix.matrix, [[0, 1], [1, 0]])

        with self.assertRaises(ValueError) as cm:
            data_invalid_size = [[0, 1, 0], [1, 0, 1]]
            matrix.init_from_list(data_invalid_size)
        self.assertIn("Input data must be 2x2", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            data_invalid_element = [[0, 2], [1, 0]]
            matrix.init_from_list(data_invalid_element)
        self.assertIn("Matrix elements must be 0 or 1.", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            data_invalid_element_type = [[0, 'a'], [1, 0]]
            matrix.init_from_list(data_invalid_element_type)
        self.assertIn("Matrix elements must be 0 or 1.", str(cm.exception))

    def test_get_word(self):
        matrix = DiagonalMatrix(size=3)
        # Заполним матрицу для предсказуемых результатов
        matrix._matrix = [[0, 1, 0],
                          [0, 0, 1],
                          [1, 0, 0]]
        # Word j=0: _matrix[(0+0)%3][0], _matrix[(1+0)%3][0], _matrix[(2+0)%3][0] => _matrix[0][0], _matrix[1][0], _matrix[2][0] => [0, 0, 1]
        self.assertEqual(matrix.get_word(0), [0, 0, 1])
        # Word j=1: _matrix[(0+1)%3][1], _matrix[(1+1)%3][1], _matrix[(2+1)%3][1] => _matrix[1][1], _matrix[2][1], _matrix[0][1] => [0, 0, 1]
        self.assertEqual(matrix.get_word(1), [0, 0, 1])
        # Word j=2: _matrix[(0+2)%3][2], _matrix[(1+2)%3][2], _matrix[(2+2)%3][2] => _matrix[2][2], _matrix[0][2], _matrix[1][2] => [0, 0, 1]
        self.assertEqual(matrix.get_word(2), [0, 0, 1])

        with self.assertRaises(IndexError) as cm:
            matrix.get_word(3)
        self.assertIn("Word index j must be between 0 and 2", str(cm.exception))

        with self.assertRaises(IndexError) as cm:
            matrix.get_word(-1)
        self.assertIn("Word index j must be between 0 and 2", str(cm.exception))

    def test_get_column(self):
        matrix = DiagonalMatrix(size=3)
        matrix._matrix = [[0, 1, 0],
                          [0, 0, 1],
                          [1, 0, 0]]
        # Column j=0: _matrix[(0+0)%3][0], _matrix[(1+0)%3][1], _matrix[(2+0)%3][2] => _matrix[0][0], _matrix[1][1], _matrix[2][2] => [0, 0, 0]
        self.assertEqual(matrix.get_column(0), [0, 0, 0])
        # Column j=1: _matrix[(0+1)%3][0], _matrix[(1+1)%3][1], _matrix[(2+1)%3][2] => _matrix[1][0], _matrix[2][1], _matrix[0][2] => [0, 0, 0]
        self.assertEqual(matrix.get_column(1), [0, 0, 0])
        # Column j=2: _matrix[(0+2)%3][0], _matrix[(1+2)%3][1], _matrix[(2+2)%3][2] => _matrix[2][0], _matrix[0][1], _matrix[1][2] => [1, 1, 1]
        self.assertEqual(matrix.get_column(2), [1, 1, 1])

        with self.assertRaises(IndexError) as cm:
            matrix.get_column(3)
        self.assertIn("Column index j must be between 0 and 2", str(cm.exception))

        with self.assertRaises(IndexError) as cm:
            matrix.get_column(-1)
        self.assertIn("Column index j must be between 0 and 2", str(cm.exception))

    def test_write_word(self):
        matrix = DiagonalMatrix(size=3)
        initial_matrix = [[False, False, False],
                          [False, False, False],
                          [False, False, False]]
        matrix.init_from_list(initial_matrix)

        word_to_write = [1, 0, 1]
        matrix.write_word(0, word_to_write)
        # Expected changes for j=0:
        # _matrix[0][0] = word[0] (1)
        # _matrix[1][0] = word[1] (0)
        # _matrix[2][0] = word[2] (1)
        self.assertEqual(matrix.matrix, [[1, False, False],
                                         [0, False, False],
                                         [1, False, False]])

        matrix.write_word(1, [0, 1, 0])
        # Expected changes for j=1:
        # _matrix[1][1] = word[0] (0)
        # _matrix[2][1] = word[1] (1)
        # _matrix[0][1] = word[2] (0)
        self.assertEqual(matrix.matrix, [[1, 0, False],
                                         [0, 0, False],
                                         [1, 1, False]])

        with self.assertRaises(ValueError) as cm:
            matrix.write_word(0, [1, 0])
        self.assertIn("Word length must be 3", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            matrix.write_word(0, [1, 0, 2])
        self.assertIn("Word elements must be 0 or 1.", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            matrix.write_word(0, [1, 0, 'a'])
        self.assertIn("Word elements must be 0 or 1.", str(cm.exception))

    def test_f0(self):
        matrix = DiagonalMatrix(size=4)
        self.assertEqual(matrix.f0(0, 0), [False, False, False, False])
        self.assertEqual(matrix.f0(100, 200), [False, False, False, False])  # Indices don't matter for f0

    def test_f5(self):
        matrix = DiagonalMatrix(size=3)
        matrix._matrix = [[1, 2, 3],
                          [4, 5, 6],
                          [7, 8, 9]]  # Using arbitrary values to check word retrieval
        # Based on get_word implementation
        self.assertEqual(matrix.f5(0, 1), matrix.get_word(1))
        self.assertEqual(matrix.f5(5, 2), matrix.get_word(2))

    def test_f10(self):
        matrix = DiagonalMatrix(size=3)
        matrix._matrix = [[0, 1, 0],
                          [0, 0, 1],
                          [1, 0, 0]]
        # get_word(0) returns [0, 0, 1]
        # f10(0, 0) should return [not 0, not 0, not 1] = [1, 1, 0]
        self.assertEqual(matrix.f10(0, 0), [True, True, False])

        # get_word(1) returns [0, 0, 1]
        # f10(0, 1) should return [not 0, not 0, not 1] = [1, 1, 0]
        self.assertEqual(matrix.f10(0, 1), [True, True, False])

    def test_f15(self):
        matrix = DiagonalMatrix(size=4)
        self.assertEqual(matrix.f15(0, 0), [True, True, True, True])
        self.assertEqual(matrix.f15(100, 200), [True, True, True, True])  # Indices don't matter for f15

    def test_matrix_property(self):
        matrix = DiagonalMatrix(size=2)
        initial_data = [[1, 0], [0, 1]]
        matrix.init_from_list(initial_data)
        retrieved_matrix = matrix.matrix
        self.assertEqual(retrieved_matrix, initial_data)
        # Ensure it's a copy, not the original reference
        retrieved_matrix[0][0] = 5
        self.assertEqual(matrix.matrix, initial_data)


    def test_sum_V(self):
        w0_before = [int(i) for i in self.matrix.get_word(0)]
        self.matrix.sum_V([1, 1, 1])
        w0_after = self.matrix.get_word(0)
        Aj = int(''.join(map(str, w0_before[3:7])), 2)
        Bj = int(''.join(map(str, w0_before[7:11])), 2)
        sum_bits = list(map(int, f"{(Aj + Bj):05b}"))
        self.assertEqual(w0_after[11:16], sum_bits)

    def test_find_nearest(self):
        matrix = DiagonalMatrix(size=4)
        w0 = matrix.get_word(0)
        matrix.write_word(2, w0)
        self.assertEqual(matrix.search_by_correspondence(0, direction="bottom"), 3)
        self.assertEqual(matrix.search_by_correspondence(0, direction="top"), 1)




if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)