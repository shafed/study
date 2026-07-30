def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return abs(a)


pairs = [(130, 15), (374, 32), (5741, 76), (846, 42), (5783, 3420)]

for a, b in pairs:
    print(f"НОД({a}, {b}) = {gcd(a, b)}")
