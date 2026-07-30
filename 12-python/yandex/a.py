import bisect

n, k = map(int, input().split())
a = list(map(int, input().split()))

cnt = n - bisect.bisect_left(a[::-1], k)

print(cnt)
