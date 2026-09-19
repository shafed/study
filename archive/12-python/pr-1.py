n = int(input("n: "))
x = int(input("x: "))
y = 0

# Циклическая реализация
fact = 1
sign = 1
degree = 1
for i in range(n + 1):
    y += sign * degree / fact
    fact *= (2 * i + 1) * (2 * i + 2)
    sign *= -1
    degree *= x * x
print(y)


# Реализация через функции
def power(base, exp):
    res = 1
    for i in range(exp):
        res *= base
    return res


def factorial(n):
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res


def solve(x, n):
    y = 0
    sign = 1
    for i in range(n + 1):
        x_n = power(x, 2 * i)
        fact = factorial(2 * i)
        y += sign * x_n / fact
        sign *= -1
    return y


print(solve(x, n))

# Рекурсивная реализация


def pow(base, exp):
    if exp == 0:
        return 1
    return base * pow(base, exp - 1)


def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)


def solve_2(x, n):
    y = pow(-1, n) * pow(x, 2 * n) / fact(2 * n)
    if n == 0:
        return y
    return y + solve_2(x, n - 1)


print(solve_2(x, n))
