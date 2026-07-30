def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0

    d, s1, t1 = extended_gcd(b, a % b)

    s = t1
    t = s1 - (a // b) * t1

    return d, s, t


pairs = [(57, 14), (328, 36), (1179, 27), (502, 52), (791, 13)]

for a, b in pairs:
    d, s, t = extended_gcd(a, b)

    print(f"a = {a}, b = {b}")
    print(f"НОД = {d}")
    print(f"s = {s}, t = {t}")
    print(f"{s} * {a} + {t} * {b} = {s * a + t * b}")
    print()
