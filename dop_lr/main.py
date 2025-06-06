from fibonacci_heap import FibonacciHeap

if __name__ == "__main__":
    heap = FibonacciHeap()

    print("\nВставляем элементы:")
    nodes = {}
    nodes['A'] = heap.insert(10, "Десять")
    nodes['B'] = heap.insert(3, "Три")
    nodes['C'] = heap.insert(15, "Пятнадцать")
    nodes['D'] = heap.insert(5, "Пять")
    nodes['E'] = heap.insert(20, "Двадцать")
    nodes['F'] = heap.insert(1, "Один")

    print(f"Минимальный элемент: {heap.minimum().key} (значение: {heap.minimum().value})")
    print(f"Количество узлов: {heap.num_nodes}")

    print("\nИзвлекаем минимальный элемент:")
    min_extracted = heap.extract_min()
    print(f"Извлечено: {min_extracted.key} (значение: {min_extracted.value})")
    print(f"Новый минимальный элемент: {heap.minimum().key} (значение: {heap.minimum().value})")
    print(f"Количество узлов: {heap.num_nodes}")

    print("\nУменьшаем ключ узла 'C' (15) до 2:")
    heap.decrease_key(nodes['C'], 2)
    print(f"Новый минимальный элемент: {heap.minimum().key} (значение: {heap.minimum().value})")

    print("\nУдаляем узел 'D' (5):")
    heap.delete(nodes['D'])
    print(f"Новый минимальный элемент: {heap.minimum().key} (значение: {heap.minimum().value})")
    print(f"Количество узлов: {heap.num_nodes}")

    print("\nСоздаем вторую кучу для объединения:")
    heap2 = FibonacciHeap()
    heap2.insert(7, "Семь")
    heap2.insert(4, "Четыре")

    print(f"Минимальный элемент второй кучи: {heap2.minimum().key}")

    print("\nОбъединяем две кучи:")
    heap.union(heap2)
    print(f"Минимальный элемент объединенной кучи: {heap.minimum().key} (значение: {heap.minimum().value})")
    print(f"Количество узлов в объединенной куче: {heap.num_nodes}")

    print("\nИзвлекаем все элементы для проверки:")
    while not heap.is_empty():
        node = heap.extract_min()
        print(f"Извлечено: {node.key} (значение: {node.value})")
