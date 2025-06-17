class DiagonalMatrix:
    def __init__(self, size=16):
        self._size = size
        self._matrix = [[0] * size for _ in range(size)]  # Используем 0 и 1 вместо bool

    def __str__(self):
        result = ''
        for row in self._matrix:
            result += f'{row}\n'
        return result

    def init_from_list(self, data: list[list[int]]):
        if len(data) != self._size or any(len(row) != self._size for row in data):
            raise ValueError(f'Input data must be {self._size}x{self._size}')

        for r_idx, row in enumerate(data):
            for c_idx, val in enumerate(row):
                if val not in [0, 1]:
                    raise ValueError("Matrix elements must be 0 or 1.")
                self._matrix[r_idx][c_idx] = val

    def get_word(self, j: int) -> list[int]:
        if not (0 <= j < self._size):
            raise IndexError(f"Word index j must be between 0 and {self._size - 1}")
        return [self._matrix[(i + j) % self._size][j] for i in range(self._size)]

    def get_column(self, j: int) -> list[int]:
        if not (0 <= j < self._size):
            raise IndexError(f"Column index j must be between 0 and {self._size - 1}")
        return [self._matrix[(i + j) % self._size][i] for i in range(self._size)]

    def write_word(self, j: int, word: list[int]):
        if len(word) != self._size:
            raise ValueError(f'Word length must be {self._size}')
        if any(bit not in [0, 1] for bit in word):
            raise ValueError("Word elements must be 0 or 1.")

        for i in range(self._size):
            self._matrix[(i + j) % self._size][j] = word[i]

    def f0(self, index1: int, index2: int) -> list[int]:
        return [0 for _ in range(self._size)]

    def f5(self, index1: int, index2: int) -> list[int]:
        return self.get_word(index2)

    def f10(self, index1: int, index2: int) -> list[int]:
        return [1 - bit for bit in self.get_word(index2)]  # Инверсия: 0 → 1, 1 → 0

    def f15(self, index1: int, index2: int) -> list[int]:
        return [1 for _ in range(self._size)]

    @property
    def matrix(self) -> list[list[int]]:
        return [row.copy() for row in self._matrix]

    def search_by_correspondence(self, reference_index, direction="top"):
        def calculate_distance(current_idx, ref_idx):
            return (current_idx - ref_idx) % self._size

        def is_valid_top_search(distance):
            return distance <= self._size // 2

        def is_valid_bottom_search(distance):
            return distance > self._size // 2

        def get_effective_distance(distance, search_dir):
            if search_dir == "top":
                return distance
            return self._size - distance

        target_word = self.get_word(reference_index)
        result_index = -1
        min_distance = float('inf')

        for current_index in range(self._size):
            if current_index == reference_index:
                continue

            current_word = self.get_word(current_index)
            if current_word != target_word:
                continue

            distance = calculate_distance(current_index, reference_index)

            if direction == "top" and not is_valid_top_search(distance):
                continue
            if direction == "bottom" and not is_valid_bottom_search(distance):
                continue

            effective_distance = get_effective_distance(distance, direction)

            if effective_distance < min_distance:
                min_distance = effective_distance
                result_index = current_index

        return result_index

    def sum_V(self, V: list[int]):
        if self._size != 16:
            raise ValueError("Matrix size must be 16 to perform this operation")

        def binary_list_to_int(binary_list: list[int]) -> int:
            return int(''.join(map(str, binary_list)), 2)

        def int_to_binary_list(number: int, bits=5) -> list[int]:
            return [int(b) for b in f"{number:0{bits}b}"[-bits:]]

        for i in range(self._size):
            word = self.get_word(i)
            if word[:3] == V:
                Aj = binary_list_to_int(word[3:7])
                Bj = binary_list_to_int(word[7:11])
                Sj = Aj + Bj
                new_word = word[:11] + int_to_binary_list(Sj)
                self.write_word(i, new_word)