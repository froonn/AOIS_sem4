import unittest

from hash_table.hash_table.balanced_tree import BalancedTree

class TestBalancedTree(unittest.TestCase):
    def setUp(self):
        self.tree = BalancedTree()

    def test_insert_and_get(self):
        self.tree.insert(1, 'a')
        self.assertEqual(self.tree.get(1), 'a')
        self.assertIsNone(self.tree.get(2))

    def test_size_property(self):
        self.assertEqual(self.tree.size, 0)
        self.tree.insert(1, 'a')
        self.assertEqual(self.tree.size, 1)
        self.tree.insert(1, 'b')
        self.assertEqual(self.tree.size, 1)

    def test_remove_existing_key(self):
        self.tree.insert(1, 'a')
        self.tree.remove(1)
        self.assertEqual(self.tree.size, 0)
        self.assertIsNone(self.tree.get(1))

    def test_remove_non_existing_key(self):
        self.tree.insert(1, 'a')
        self.tree.remove(2)
        self.assertEqual(self.tree.size, 1)
        self.assertEqual(self.tree.get(1), 'a')

    def test_balance_after_insertions(self):
        keys = [3, 2, 1]
        for k in keys:
            self.tree.insert(k, str(k))
        root = self.tree._root
        self.assertEqual(root.key, 2)
        self.assertEqual(root.left.key, 1)
        self.assertEqual(root.right.key, 3)
        self.assertTrue(self._is_balanced(root))

    def test_balance_after_removals(self):
        keys = [5, 3, 7, 2, 4, 6, 8]
        for k in keys:
            self.tree.insert(k, str(k))
        self.tree.remove(5)
        self.tree.remove(6)
        self.assertTrue(self._is_balanced(self.tree._root))
        self.assertEqual(self.tree.size, 5)

    def test_in_order_traversal(self):
        keys = [5, 3, 7, 2, 4, 6, 8]
        for k in keys:
            self.tree.insert(k, str(k))
        in_order = self._get_in_order(self.tree._root)
        self.assertEqual(in_order, sorted(keys))

    def test_node_heights(self):
        self.tree.insert(10, 'a')
        self.tree.insert(20, 'b')
        self.tree.insert(30, 'c')
        root = self.tree._root
        self.assertEqual(root.height, 2)
        self.assertEqual(root.left.height, 1)
        self.assertEqual(root.right.height, 1)

    def test_complex_operations(self):
        for i in range(10):
            self.tree.insert(i, str(i))
        for i in range(5):
            self.tree.remove(i)
        self.assertEqual(self.tree.size, 5)
        self.assertTrue(self._is_balanced(self.tree._root))
        self._check_height_property(self.tree._root)
        self._check_balance_factors(self.tree._root)

    def _is_balanced(self, node):
        if not node:
            return True
        left_height = BalancedTree._height(node.left)
        right_height = BalancedTree._height(node.right)
        if abs(left_height - right_height) > 1:
            return False
        return self._is_balanced(node.left) and self._is_balanced(node.right)

    def _get_in_order(self, node):
        result = []
        if node:
            result.extend(self._get_in_order(node.left))
            result.append(node.key)
            result.extend(self._get_in_order(node.right))
        return result

    def _check_height_property(self, node):
        if not node:
            return 0
        left_height = self._check_height_property(node.left)
        right_height = self._check_height_property(node.right)
        self.assertEqual(node.height, 1 + max(left_height, right_height))
        return node.height

    def _check_balance_factors(self, node):
        if not node:
            return
        balance = BalancedTree._height(node.left) - BalancedTree._height(node.right)
        self.assertTrue(-1 <= balance <= 1)
        self._check_balance_factors(node.left)
        self._check_balance_factors(node.right)

if __name__ == '__main__':
    unittest.main()