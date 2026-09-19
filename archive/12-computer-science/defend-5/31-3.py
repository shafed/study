def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0

    d, s1, t1 = extended_gcd(b, a % b)

    s = t1
    t = s1 - (a // b) * t1

    return d, s, t


def solve_diophantine(a, b, c):
    d, s, t = extended_gcd(a, b)

    if c % d != 0:
        return None

    multiplier = c // d

    x0 = s * multiplier
    y0 = t * multiplier

    step_x = b // d
    step_y = a // d

    return d, x0, y0, step_x, step_y


equations = [(25, 10, 15), (19, 13, 20), (14, 21, 77), (40, 16, 88)]

for a, b, c in equations:
    result = solve_diophantine(a, b, c)

    print(f"{a}x + {b}y = {c}")

    if result is None:
        print("Целых решений нет")
    else:
        d, x0, y0, step_x, step_y = result

        print(f"НОД = {d}")
        print(f"Частное решение: x0 = {x0}, y0 = {y0}")
        print("Общее решение:")
        print(f"x = {x0} + {step_x}k")
        print(f"y = {y0} - {step_y}k")

    print()
