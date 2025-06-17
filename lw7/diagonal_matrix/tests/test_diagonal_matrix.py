import unittest

from diagonal_matrix import DiagonalMatrix


class TestDiagonalMatrix(unittest.TestCase):
    def setUp(self):
        self.matrix = DiagonalMatrix(4)
        test_data = [
            [1, 0, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        self.matrix.init_from_list(test_data)

    def test_initialization(self):
        m = DiagonalMatrix()
        self.assertEqual(len(m.matrix), 16)
        self.assertEqual(len(m.matrix[0]), 16)

        with self.assertRaises(ValueError):
            m.init_from_list([[1, 0], [0, 1]])

    def test_get_word(self):

        self.assertEqual(self.matrix.get_word(0), [1, 0, 0, 0])
        self.assertEqual(self.matrix.get_word(1), [1, 0, 0, 0])
        self.assertEqual(self.matrix.get_word(2), [1, 0, 0, 0])
        self.assertEqual(self.matrix.get_word(3), [1, 0, 1, 0])

        with self.assertRaises(IndexError):
            self.matrix.get_word(-1)
            self.matrix.get_word(4)

    def test_write_word(self):

        new_word = [1, 1, 0, 1]
        self.matrix.write_word(2, new_word)
        self.assertEqual(self.matrix.get_word(2), new_word)

        with self.assertRaises(ValueError):
            self.matrix.write_word(0, [1, 0])
            self.matrix.write_word(0, [1, 2, 0, 1])

    def test_get_column(self):
        self.assertEqual(self.matrix.get_column(0), [1, 1, 1, 1])
        self.assertEqual(self.matrix.get_column(1), [0, 0, 0, 0])
        self.assertEqual(self.matrix.get_column(2), [0, 0, 0, 1])
        self.assertEqual(self.matrix.get_column(3), [0, 0, 0, 0])

    def test_logic_functions(self):
        self.assertEqual(self.matrix.f0(0, 0), [0, 0, 0, 0])
        self.assertEqual(self.matrix.f5(0, 1), [1, 0, 0, 0])
        self.assertEqual(self.matrix.f10(0, 0), [0, 1, 1, 1])
        self.assertEqual(self.matrix.f15(0, 0), [1, 1, 1, 1])

    def test_search_by_correspondence(self):
        search_matrix = DiagonalMatrix(4)
        test_data = [
            [1, 0, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        search_matrix.init_from_list(test_data)

        self.assertEqual(search_matrix.search_by_correspondence(1, "top"), 2)
        self.assertEqual(search_matrix.search_by_correspondence(1, "bottom"), 0)
        self.assertEqual(search_matrix.search_by_correspondence(3, "top"), -1)

    def test_sum_V(self):
        sum_matrix = DiagonalMatrix(16)
        test_word = [1, 0, 1] + [0, 1, 1, 0] + [1, 0, 0, 1] + [0, 0, 0, 0, 0]
        for i in range(16):
            sum_matrix.write_word(i, test_word)

        sum_matrix.sum_V([1, 0, 1])

        for i in range(16):
            word = sum_matrix.get_word(i)
            print(word)
            if word[:3] == [1, 0, 1]:
                self.assertEqual(word[11:16], [0, 1, 1, 1, 1])



if __name__ == '__main__':
    unittest.main()