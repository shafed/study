# 2. Найдите соотношение положительных чисел, отрицательных чисел и нулей в массиве целых чисел. Пример: [0, 1, 2, –1, –5, 6, 0, –3, –2, 3, 4, 6, 8] → (0.54, 0.31, 0.15). Необходимо реализовать задачу, используя знания о функциях высшего порядка.

import random

arr = [random.randint(-10, 11) for _ in range(10)]
print(arr)

res = (
    len(list(filter(lambda x: x > 0, arr))) / len(arr),
    len(list(filter(lambda x: x < 0, arr))) / len(arr),
    len(list(filter(lambda x: x == 0, arr))) / len(arr),
)
res2 = tuple(
    map(
        lambda f: len(list(filter(f, arr))) / len(arr),
        [lambda x: x > 0, lambda x: x < 0, lambda x: x == 0],
    )
)
print(res)
print(res2)
