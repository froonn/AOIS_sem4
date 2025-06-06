import unittest

from fibonacci_heap import *


# --- Unit Tests ---
class TestFibonacciHeap(unittest.TestCase):
    """
    Class for testing the FibonacciHeap implementation.
    """

    def setUp(self):
        """
        Setup for each test: create a new heap.
        """
        self.heap = FibonacciHeap()

    def test_initial_state(self):
        """
        Test the initial state of the heap.
        """
        self.assertTrue(self.heap.is_empty())
        self.assertIsNone(self.heap.minimum())
        self.assertEqual(self.heap.num_nodes, 0)

    def test_insert_and_minimum(self):
        """
        Test inserting elements and the minimum() function.
        """
        node10 = self.heap.insert(10)
        self.assertEqual(self.heap.minimum().key, 10)
        self.assertEqual(self.heap.num_nodes, 1)
        self.assertFalse(self.heap.is_empty())

        node3 = self.heap.insert(3)
        self.assertEqual(self.heap.minimum().key, 3)
        self.assertEqual(self.heap.num_nodes, 2)

        node15 = self.heap.insert(15)
        self.assertEqual(self.heap.minimum().key, 3)
        self.assertEqual(self.heap.num_nodes, 3)

        node1 = self.heap.insert(1)
        self.assertEqual(self.heap.minimum().key, 1)
        self.assertEqual(self.heap.num_nodes, 4)

    def test_extract_min(self):
        """
        Test extracting the minimum element.
        """
        self.heap.insert(10)
        self.heap.insert(3)
        self.heap.insert(15)
        self.heap.insert(1) # Min node

        extracted = self.heap.extract_min()
        self.assertEqual(extracted.key, 1)
        self.assertEqual(self.heap.num_nodes, 3)
        self.assertEqual(self.heap.minimum().key, 3)

        extracted = self.heap.extract_min()
        self.assertEqual(extracted.key, 3)
        self.assertEqual(self.heap.num_nodes, 2)
        self.assertEqual(self.heap.minimum().key, 10)

        self.heap.extract_min()
        self.heap.extract_min()
        self.assertTrue(self.heap.is_empty())
        self.assertIsNone(self.heap.minimum())
        self.assertIsNone(self.heap.extract_min()) # Extracting from an empty heap

    def test_decrease_key(self):
        """
        Test decreasing a key.
        """
        node10 = self.heap.insert(10, "A")
        node3 = self.heap.insert(3, "B")
        node15 = self.heap.insert(15, "C") # Node whose key we will decrease
        node5 = self.heap.insert(5, "D")

        self.assertEqual(self.heap.minimum().key, 3)

        # Decrease key 15 to 2
        self.heap.decrease_key(node15, 2)
        self.assertEqual(node15.key, 2)
        self.assertEqual(self.heap.minimum().key, 2) # New minimum
        self.assertEqual(self.heap.num_nodes, 4)

        # Decrease key 10 to 1
        self.heap.decrease_key(node10, 1)
        self.assertEqual(node10.key, 1)
        self.assertEqual(self.heap.minimum().key, 1) # New minimum
        self.assertEqual(self.heap.num_nodes, 4)

        # Attempt to increase the key - should raise an error
        with self.assertRaises(ValueError):
            self.heap.decrease_key(node3, 20)

    def test_delete(self):
        """
        Test deleting a node.
        """
        node10 = self.heap.insert(10)
        node3 = self.heap.insert(3)
        node15 = self.heap.insert(15)
        node5 = self.heap.insert(5)

        self.assertEqual(self.heap.num_nodes, 4)
        self.assertEqual(self.heap.minimum().key, 3)

        # Delete node with key 5 (node5).
        # The delete method changes the node’s key to -inf before extracting.
        deleted_node = self.heap.delete(node5)
        self.assertEqual(deleted_node.key, float('-inf')) # Check that the extracted node has key -inf
        self.assertEqual(self.heap.num_nodes, 3)
        self.assertEqual(self.heap.minimum().key, 3) # Minimum did not change

        # Delete the minimum node (node3)
        deleted_node = self.heap.delete(node3)
        self.assertEqual(deleted_node.key, float('-inf')) # Check that the extracted node has key -inf
        self.assertEqual(self.heap.num_nodes, 2)
        self.assertEqual(self.heap.minimum().key, 10) # New minimum

        # Extract remaining nodes to ensure they are correct and the heap is empty
        extracted_keys = []
        while not self.heap.is_empty():
            extracted_keys.append(self.heap.extract_min().key)
        self.assertEqual(sorted(extracted_keys), [10, 15]) # Keys left after removing 5 and 3

    def test_union(self):
        """
        Test merging two heaps.
        """
        heap1 = FibonacciHeap()
        heap1.insert(10)
        heap1.insert(3)
        heap1.insert(15)

        heap2 = FibonacciHeap()
        heap2.insert(7)
        heap2.insert(4)
        heap2.insert(1)

        self.assertEqual(heap1.num_nodes, 3)
        self.assertEqual(heap2.num_nodes, 3)
        self.assertEqual(heap1.minimum().key, 3)
        self.assertEqual(heap2.minimum().key, 1)

        unified_heap = heap1.union(heap2)

        self.assertEqual(unified_heap.num_nodes, 6)
        self.assertEqual(unified_heap.minimum().key, 1) # Minimum of the joined heaps

        # Check that elements from both heaps can be extracted
        extracted_keys = []
        while not unified_heap.is_empty():
            extracted_keys.append(unified_heap.extract_min().key)
        self.assertEqual(sorted(extracted_keys), [1, 3, 4, 7, 10, 15])

    def test_union_with_empty_heap(self):
        """
        Test merging with an empty heap.
        """
        heap1 = FibonacciHeap()
        heap1.insert(5)
        heap1.insert(2)

        empty_heap = FibonacciHeap()

        unified_heap1 = heap1.union(empty_heap)
        self.assertEqual(unified_heap1.num_nodes, 2)
        self.assertEqual(unified_heap1.minimum().key, 2)

        unified_heap2 = empty_heap.union(heap1) # Merging empty with non-empty
        self.assertEqual(unified_heap2.num_nodes, 2)
        self.assertEqual(unified_heap2.minimum().key, 2)

    def test_complex_operations_sequence(self):
        """
        Test a sequence of various operations.
        """
        nodes = {}
        nodes['A'] = self.heap.insert(10)
        nodes['B'] = self.heap.insert(3)
        nodes['C'] = self.heap.insert(15)
        nodes['D'] = self.heap.insert(5)
        nodes['E'] = self.heap.insert(20)
        nodes['F'] = self.heap.insert(1)

        self.assertEqual(self.heap.minimum().key, 1)
        self.assertEqual(self.heap.num_nodes, 6)

        self.heap.extract_min() # Extract 1
        self.assertEqual(self.heap.minimum().key, 3)
        self.assertEqual(self.heap.num_nodes, 5)

        self.heap.decrease_key(nodes['C'], 2) # Decrease 15 to 2
        self.assertEqual(self.heap.minimum().key, 2)
        self.assertEqual(self.heap.num_nodes, 5)

        self.heap.delete(nodes['D']) # Delete 5
        self.assertEqual(self.heap.num_nodes, 4)
        self.assertEqual(self.heap.minimum().key, 2)

        extracted_keys = []
        while not self.heap.is_empty():
            extracted_keys.append(self.heap.extract_min().key)
        self.assertEqual(sorted(extracted_keys), [2, 3, 10, 20])

if __name__ == '__main__':
    unittest.main()