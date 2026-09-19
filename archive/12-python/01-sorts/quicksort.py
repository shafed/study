def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [i for i in arr if i < pivot]
    mid = [i for i in arr if i == pivot]
    right = [i for i in arr if i > pivot]
    return quick_sort(left) + mid + quick_sort(right)
