def counting_sort(arr):
    if not arr:
        return arr
    maxval = max(arr)
    cnt = maxval * [0]
    for x in arr:
        cnt[x] += 1
    res = []
    for val, cnt in enumerate(cnt):
        res += [val] * cnt
    return res
