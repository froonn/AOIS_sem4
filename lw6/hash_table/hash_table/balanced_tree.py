class BalancedTreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class BalancedTree:
    def __init__(self):
        self._root = None
        self._size = 0

    def insert(self, key, value):
        self._root = self._insert(self._root, key, value)

    def get(self, key):
        return self._get(self._root, key)

    def remove(self, key):
        self._root = self._remove(self._root, key)

    @property
    def size(self):
        return self._size

    def _insert(self, node, key, value):
        if not node:
            self._size += 1
            return BalancedTreeNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
            return node

        self._update_height(node)
        return self._rebalance(node)

    def _get(self, node, key):
        if not node:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._get(node.left, key)
        else:
            return self._get(node.right, key)

    def _remove(self, node, key):
        if not node:
            return None
        if key < node.key:
            node.left = self._remove(node.left, key)
        elif key > node.key:
            node.right = self._remove(node.right, key)
        else:
            if not node.left:
                self._size -= 1
                return node.right
            elif not node.right:
                self._size -= 1
                return node.left
            else:
                min_node = self._find_min(node.right)
                node.key = min_node.key
                node.value = min_node.value
                node.right = self._remove(node.right, min_node.key)

        if not node:
            return None
        self._update_height(node)
        return self._rebalance(node)

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _rebalance(self, node):
        balance = self._balance_factor(node)

        if balance > 1:
            if self._balance_factor(node.left) >= 0:
                return self._rotate_right(node)
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

        if balance < -1:
            if self._balance_factor(node.right) <= 0:
                return self._rotate_left(node)
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        return node

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        self._update_height(z)
        self._update_height(y)

        return y

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        self._update_height(z)
        self._update_height(y)

        return y

    @staticmethod
    def _find_min(node):
        current = node
        while current.left:
            current = current.left
        return current

    @staticmethod
    def _height(node):
        if not node:
            return 0
        return node.height