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
