from math import floor, log2
from random import randint


def insertionsort(listt):
    n = len(listt)
    if n <= 1:
        return
    for i in range(1, n):
        key = listt[i]
        j = i - 1
        while j >= 0 and key < listt[j]:
            listt[j + 1] = listt[j]
            j -= 1
        listt[j + 1] = key


def merge(left, right):
    sorted_list = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1
    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    return sorted_list


def timsort(listt):
    n = len(listt)
    minrun = floor(log2(n)) + 1

    stack = []
    for start in range(0, n, minrun):
        run = listt[start : start + minrun]
        insertionsort(run)
        stack.append(run)

    while len(stack) > 1:
        new_stack = []
        for i in range(0, len(stack), 2):
            if i + 1 < len(stack):  # есть следующий
                new_stack.append(merge(stack[i], stack[i + 1]))
            else:
                new_stack.append(stack[i])  # нет пары
        stack = new_stack

    return stack[0]


n = randint(10, 50)
arr = [randint(1, 100) for _ in range(n)]

print(n)
print(arr)
res = timsort(arr)
print(res)
