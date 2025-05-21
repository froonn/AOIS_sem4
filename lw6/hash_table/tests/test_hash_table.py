import unittest
from unittest.mock import patch

from hash_table.hash_table.balanced_tree import BalancedTree
from hash_table.hash_table.hash_table import HashTable


class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.hash_table = HashTable(size=4)
        self.sample_keys = [('key1', 10), ('key2', 20), ('key3', 30)]

    def test_initialization(self):
        self.assertEqual(self.hash_table.size, 4)
        self.assertEqual(len(self.hash_table), 0)
        for bucket in self.hash_table._table:
            self.assertIsInstance(bucket, BalancedTree)
        self.assertSetEqual(self.hash_table.keys, set())

    def test_insert_and_get(self):
        self.hash_table.insert('key1', 10)
        self.assertEqual(len(self.hash_table), 1)
        self.assertIn('key1', self.hash_table)
        self.assertEqual(self.hash_table.get('key1'), 10)

        self.hash_table.insert('key1', 100)
        self.assertEqual(len(self.hash_table), 1)
        self.assertEqual(self.hash_table.get('key1'), 100)

    def test_get_nonexistent_key(self):
        self.assertIsNone(self.hash_table.get('nonexistent'))

    def test_remove_key(self):
        self.hash_table.insert('key1', 10)
        self.hash_table.insert('key2', 20)

        # Удаление существующего ключа
        self.hash_table.remove('key1')
        self.assertEqual(len(self.hash_table), 1)
        self.assertNotIn('key1', self.hash_table)
        self.assertIsNone(self.hash_table.get('key1'))


    def test_contains(self):
        self.hash_table.insert('key1', 10)
        self.assertTrue(self.hash_table.contains('key1'))
        self.assertFalse(self.hash_table.contains('nonexistent'))
        self.assertIn('key1', self.hash_table)
        self.assertNotIn('key2', self.hash_table)

    def test_keys_property(self):
        # Проверка, что возвращается копия списка ключей
        original_keys = self.hash_table.keys
        original_keys.add('hack')
        self.assertNotIn('hack', self.hash_table.keys)

    def test_items_property(self):
        for k, v in self.sample_keys:
            self.hash_table.insert(k, v)
        items = self.hash_table.items
        self.assertEqual(len(items), 3)
        self.assertIn(('key1', 10), items)
        self.assertIn(('key2', 20), items)
        self.assertIn(('key3', 30), items)

    @patch('hash_table.hash_table.hash_func.calculate_extended_hash')
    def test_collision_handling(self, mock_hash):
        # Все ключи будут иметь один хэш
        mock_hash.return_value = 2
        ht = HashTable(size=4)

        ht.insert('key1', 10)
        ht.insert('key2', 20)

        # Проверка коллизии
        self.assertEqual(ht.size, 4)
        self.assertEqual(len(ht), 2)
        self.assertEqual(ht._table[2].size, 2)

        # Удаление одного ключа из коллизии
        ht.remove('key1')
        self.assertEqual(ht._table[2].size, 1)
        self.assertNotIn('key1', ht)
        self.assertIn('key2', ht)

    def test_setitem_and_delitem(self):
        self.hash_table['key1'] = 10
        self.assertEqual(self.hash_table['key1'], 10)

        del self.hash_table['key1']
        self.assertNotIn('key1', self.hash_table)


if __name__ == '__main__':
    unittest.main()