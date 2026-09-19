# Шапаренко Фёдор Александрович КВБО-11-25 Вариант 4
"""01.py"""

n = int(input())
s = "На лугу пасётся "

if 11 <= n % 100 <= 14:
    s += f"{n} коней"
elif n % 10 == 1:
    s += f"{n} конь"
elif 1 < n % 10 <= 4:
    s += f"{n} коня"
elif 5 <= n % 10 <= 9 or n % 10 == 0:
    s += f"{n} коней"

print(s)

"""02.py"""


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)


arr = [6, 3, 5, 1, 8, 4, 2, 7]
print(arr)
print(quick_sort(arr))

"""03.py"""
from random import randint


# Sort from previous file
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x > pivot]  # x < pivot -> >
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x < pivot]  # x > pivot -> <
    return quick_sort(left) + mid + quick_sort(right)


arr = [randint(1, 10) for _ in range(randint(1, 10))]
print(arr)

filtered = list(filter(lambda x: x % 2 != 0, arr))
result = quick_sort(filtered)
print(result)

"""04.py"""


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, value):
        node = Node(value)
        if not self.head:
            self.head = node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = node

    def remove(self, value):
        if not self.head:
            return
        if self.head.value == value:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                return
            current = current.next

    def __repr__(self):
        result, current = [], self.head
        while current:
            result.append(str(current.value))
            current = current.next
        return " ".join(result)


ll = LinkedList()
for x in range(10):
    ll.add(x)
print("Изначальный:", ll)
ll.add(20)
ll.add(30)
ll.add(40)
print("1) Добавили:", ll)
ll.remove(5)
print("2) Убрали 5:", ll)
ll.add(101)
ll.add(366)
print("3) Добавили:", ll)
ll.remove(30)
ll.remove(366)
print("4) Удалили 30 и 366", ll)
