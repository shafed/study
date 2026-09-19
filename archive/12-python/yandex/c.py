import sys

data = sys.stdin.read().split()
n = int(data[0])
given = list(map(int, data[1::]))

km = []
for i in range(1, n):
    if given[i] - given[i - 1] != 2:
        km.append(i)

if len(km) == 1:
    print(km[0], km[0])
else:
    print(km[0], km[1])
