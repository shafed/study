from random import randint

# n = randint(1, 10)
# arr = [randint(1, 100) for _ in range(n)]
# arr = [9, 16, 14, 3, 3, 1, 1, 18, 19, 8, 2, 15, 10, 2]
arr = [19, 30, 7, 29, 13, 25, 20, 3, 17, 22, 20, 28, 19, 15, 6, 2, 2, 7, 12]
n = len(arr)

x, y = [], []
res_x, res_y = [], []
right_x, right_y = 0, 0

for i in range(1, n):
    if arr[i] >= arr[i - 1]:
        x.append(arr[i - 1])
    else:
        x.append(arr[i - 1])
        if len(x) >= len(res_x):
            right_x = i - 1
        res_x = max(x.copy(), res_x, key=len)
        x.clear()

    if arr[i] < arr[i - 1]:
        y.append(arr[i - 1])
    else:
        y.append(arr[i - 1])
        if len(y) >= len(res_y):
            right_y = i - 1
        res_y = max(y.copy(), res_y, key=len)
        y.clear()


print(arr)
if len(res_x) > len(res_y):
    left, right = right_x - len(res_x) + 1, right_x
    print(
        f"Наибольший срез списка по возрастанию {res_x} лежит в диапазоне от  {left} до {right}"
    )
else:
    left, right = right_y - len(res_y) + 1, right_y
    print(
        f"Наибольший срез списка по по убыванию: {res_y} лежит в диапазоне  от {left} до {right} позиции"
    )
