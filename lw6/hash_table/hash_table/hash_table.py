from .hash_func import calculate_extended_hash
from .balanced_tree import BalancedTree

from typing import Any

class HashTable:
    def __init__(self, size: int = 8) -> None:
        """
        Initializes a hash table with the given size.

        Args:
            size (int): The size of the hash table.
        """
        self._size: int = size
        self._keys: set[Any] = set()
        self._table: list[BalancedTree] = [BalancedTree() for _ in range(size)]

    def __len__(self) -> int:
        """
        Returns the number of elements in the hash table.

        Returns:
            int: The number of elements in the hash table.
        """
        return len(self._keys)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.insert(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def __contains__(self, key):
        return key in self._keys

    def __str__(self):
        representation = '{\n'
        for i in self._keys:
            representation += f'\t"{str(i)}" : {self._table[calculate_extended_hash(i, self._size)].get(i)},\n'
        return representation + '}'

    def get(self, key):
        return self._table[calculate_extended_hash(key, self._size)].get(key)

    def insert(self, key, value):
        self._table[calculate_extended_hash(key, self._size)].insert(key, value)
        self._keys.add(key)

    def remove(self, key):
        self._table[calculate_extended_hash(key, self._size)].remove(key)
        self._keys.remove(key)

    def contains(self, key):
        return key in self._keys

    @property
    def size(self) -> int:
        """
        Returns the size of the hash table.

        Returns:
            int: The size of the hash table.
        """
        return self._size

    @property
    def keys(self) -> set[Any]:
        """
        Returns A copy of the set of keys in the hash table.

        Returns:
            set: A copy of the set of keys in the hash table.
        """
        return self._keys.copy()

    @property
    def items(self) -> list:
        return [(i, self._table[calculate_extended_hash(i, self._size)].get(i)) for i in self._keys]

    @property
    def load_factor(self) -> float:
        return round(len(self._keys) / self._size, 2)
