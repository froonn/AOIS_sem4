import math

class FibonacciNode:
    """
    Represents a node in the Fibonacci heap.
    """
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.parent = None
        self.children = []
        self.degree = 0  # Number of children
        self.mark = False  # Whether the node is marked (for the decrease_key operation)
        self.left = self  # Pointer to the left neighbor in the root or children list
        self.right = self # Pointer to the right neighbor in the root or children list

    def __str__(self):
        return f"Node(key={self.key}, value={self.value}, degree={self.degree}, mark={self.mark})"

    def __repr__(self):
        return self.__str__()


class FibonacciHeap:
    """
    Implementation of a Fibonacci heap.
    """
    def __init__(self):
        self.min_node = None  # Pointer to the node with the minimum key
        self.num_nodes = 0    # Total number of nodes in the heap

    def is_empty(self):
        """
        Checks if the heap is empty.
        """
        return self.num_nodes == 0

    def insert(self, key, value=None):
        """
        Inserts a new node into the heap.
        """
        new_node = FibonacciNode(key, value)
        if self.min_node is None:
            self.min_node = new_node
        else:
            # Add the new node to the root list
            self._add_to_root_list(new_node)
            if new_node.key < self.min_node.key:
                self.min_node = new_node
        self.num_nodes += 1
        return new_node

    def minimum(self):
        """
        Returns the node with the minimum key.
        """
        return self.min_node

    def extract_min(self):
        """
        Extracts and returns the node with the minimum key.
        """
        z = self.min_node
        if z is not None:
            # Add z's children to the root list
            # Important: make a copy of the children since the list will be modified
            for child in list(z.children):
                self._add_to_root_list(child)
                child.parent = None # Remove the parent link
            z.children = [] # Clear extracted node's children list

            # Remove z from the root list
            self._remove_from_root_list(z)

            if z == z.right: # If z was the only node in the root list
                self.min_node = None
            else:
                self.min_node = z.right # Temporarily set min_node
                self._consolidate()     # Consolidate the heap

            self.num_nodes -= 1
        return z

    def decrease_key(self, x, new_key):
        """
        Decreases the key of node x to new_key.
        """
        if new_key > x.key:
            raise ValueError("New key is greater than current key.") # For testing

        x.key = new_key
        y = x.parent

        if y is not None and x.key < y.key:
            self._cut(x, y)
            self._cascading_cut(y)

        if x.key < self.min_node.key:
            self.min_node = x

    def delete(self, x):
        """
        Deletes node x from the heap.
        """
        # Decrease its key to the smallest possible value so it becomes the min_node
        self.decrease_key(x, float('-inf'))
        return self.extract_min() # Return the removed node

    def union(self, h2):
        """
        Merges two Fibonacci heaps.
        """
        h1 = self
        if h1.min_node is None:
            h1.min_node = h2.min_node
            h1.num_nodes = h2.num_nodes
            return h1
        if h2.min_node is None:
            return h1

        # Join root lists
        # Save links for restoring
        h1_min_right = h1.min_node.right
        h2_min_right = h2.min_node.right

        # Link h1.min_node.right with h2.min_node
        h1.min_node.right.left = h2.min_node
        h2.min_node.right = h1_min_right

        # Link h2.min_node.right with h1.min_node
        h2_min_right.left = h1.min_node
        h1.min_node.right = h2_min_right

        # Update min_node
        if h2.min_node.key < h1.min_node.key:
            h1.min_node = h2.min_node

        h1.num_nodes += h2.num_nodes
        return h1

    def _add_to_root_list(self, node):
        """
        Helper function: adds a node to the root list.
        """
        if self.min_node is None:
            self.min_node = node
            node.left = node
            node.right = node
        else:
            # Insert the node to the right of min_node
            node.right = self.min_node.right
            node.left = self.min_node
            self.min_node.right.left = node
            self.min_node.right = node

    def _remove_from_root_list(self, node):
        """
        Helper function: removes a node from the root list.
        """
        node.left.right = node.right
        node.right.left = node.left

    def _link(self, y, x):
        """
        Helper function: makes y a child of x.
        x becomes y's parent.
        """
        self._remove_from_root_list(y) # Remove y from root list
        x.children.append(y)
        y.parent = x
        x.degree += 1
        y.mark = False

    def _consolidate(self):
        """
        Helper function: consolidates the root list.
        """
        max_degree = int(self._log_base_phi(self.num_nodes)) + 1 if self.num_nodes > 0 else 0
        A = [None] * (max_degree + 1) # Array for nodes, indexed by degree

        root_list = []
        current = self.min_node
        if current:
            # Gather all nodes in the root list
            start_node = current
            while True:
                root_list.append(current)
                current = current.right
                if current == start_node:
                    break

        # Clear the root list before reconstruction
        self.min_node = None

        for w in root_list:
            x = w
            d = x.degree
            while A[d] is not None:
                y = A[d] # Another node with the same degree
                if x.key > y.key:
                    x, y = y, x # Ensure x has the smaller key
                self._link(y, x) # Make y a child of x
                A[d] = None
                d += 1
            A[d] = x

        for i in range(len(A)):
            if A[i] is not None:
                if self.min_node is None:
                    # Initialize a new root list
                    self.min_node = A[i]
                    self.min_node.left = self.min_node
                    self.min_node.right = self.min_node
                else:
                    # Add node to new root list
                    self._add_to_root_list(A[i])
                    # Update min_node if a smaller one is found
                    if A[i].key < self.min_node.key:
                        self.min_node = A[i]

    def _cut(self, x, y):
        """
        Helper function: cuts node x from its parent y.
        Adds x to the root list.
        """
        y.children.remove(x)
        y.degree -= 1
        self._add_to_root_list(x)
        x.parent = None
        x.mark = False

    def _cascading_cut(self, y):
        """
        Helper function: performs a cascading cut.
        """
        z = y.parent
        if z is not None:
            if not y.mark:
                y.mark = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)

    def _log_base_phi(self, n):
        """
        Helper function: computes the logarithm with the golden ratio (phi) as the base.
        """
        phi = (1 + math.sqrt(5)) / 2
        return math.log(n, phi) if n > 0 else 0