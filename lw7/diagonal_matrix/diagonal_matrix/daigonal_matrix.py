class DiagonalMatrix:
    def __init__(self, size=16):
        self._size = size
        self._matrix = [[False] * size for _ in range(size)]

    def __str__(self):
        result = ''
        for row in self._matrix:
            result += f'{[int(i) for i in row]}\n'
        return result

    def init_from_list(self, data: list[list[int]]):
        if len(data) != self._size or any(len(row) != self._size for row in data):
            raise ValueError(f'Input data must be {self._size}x{self._size}')

        for r_idx, row in enumerate(data):
            for c_idx, val in enumerate(row):
                if val not in [0, 1, False, True]:
                    raise ValueError("Matrix elements must be 0 or 1.")
                self._matrix[r_idx][c_idx] = bool(val)

    def get_word(self, j: int) -> list[bool]:
        if not (0 <= j < self._size):
            raise IndexError(f"Word index j must be between 0 and {self._size - 1}")
        return [self._matrix[(i + j) % self._size][j] for i in range(self._size)]

    def get_column(self, j: int) -> list[bool]:
        if not (0 <= j < self._size):
            raise IndexError(f"Column index j must be between 0 and {self._size - 1}")
        return [self._matrix[(i + j) % self._size][i] for i in range(self._size)]

    def write_word(self, j: int, word: list[bool]):
        if len(word) != self._size:
            raise ValueError(f'Word length must be {self._size}')
        if any(bit not in [0, 1] for bit in word):
            raise ValueError("Word elements must be 0 or 1.")

        for i in range(self._size):
            self._matrix[(i + j) % self._size][j] = word[i]

    def f0(self, index1: int, index2: int) -> list[bool]:
        return [False for _ in range(self._size)]

    def f5(self, index1: int, index2: int) -> list[bool]:
        return self.get_word(index2)

    def f10(self, index1: int, index2: int) -> list[bool]:
        return [not i for i in self.get_word(index2)]

    def f15(self, index1: int, index2: int) -> list[bool]:
        return [True for _ in range(self._size)]

    @property
    def matrix(self) -> list[list[bool]]:
        return [row.copy() for row in self._matrix]


    def search_by_correspondence(self, reference_index, direction="top"):
        target_word = self.get_word(reference_index)
        nearest_index = -1
        min_distance = float('inf')

        for j in range(self._size):
            if j == reference_index:
                continue
            if self.get_word(j) == target_word:
                distance = (j - reference_index) % self._size

                if direction == "top":
                    if distance > (self._size // 2):
                        continue
                    if distance < min_distance:
                        min_distance = distance
                        nearest_index = j
                elif direction == "bottom":
                    if distance <= (self._size // 2):
                        continue
                    adjusted_distance = self._size - distance
                    if adjusted_distance < min_distance:
                        min_distance = adjusted_distance
                        nearest_index = j

        return nearest_index

    def sum_V(self, V):
        if self._size != 16:
            raise ValueError("Matrix size must be 16 to perform this operation")
        for j in range(self._size):
            word = [int(i) for i in self.get_word(j)]
            if word[:3] == V:
                Aj = int(''.join(map(str, word[3:7])), 2)
                Bj = int(''.join(map(str, word[7:11])), 2)
                S_new = Aj + Bj
                S_bits = list(map(int, f"{S_new:05b}"))[-5:]

                Aj_bits = list(map(int, f"{Aj:04b}"))
                Bj_bits = list(map(int, f"{Bj:04b}"))
                new_word = word[:3] + Aj_bits + Bj_bits + S_bits
                self.write_word(j, new_word)