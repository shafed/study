def fermat_test(n, base=2):
    if n <= 1:
        return False

    return pow(base, n - 1, n) == 1


numbers = [100, 110, 130, 150, 200, 250, 271, 341, 561]

passed = []

for n in numbers:
    if fermat_test(n, 2):
        passed.append(n)

print("Числа, прошедшие испытание Ферма:", passed)
print("Количество:", len(passed))
