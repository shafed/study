def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def separate(n):
    for p in range(2, n):
        if is_prime(p) and is_prime(n - p):
            return p, n - p


n = int(input())

if is_prime(n):
    print(1)
    print(n)
elif is_prime(n - 2):
    print(2)
    print(2, n - 2)
else:
    p, q = separate(n) if n % 2 == 0 else (0, 0)
    if p:
        print(2)
        print(p, q)
    else:
        p, q = separate(n - 3)
        print(3)
        print(3, p, q)
