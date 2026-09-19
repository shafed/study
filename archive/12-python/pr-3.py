# Шапаренко Федор КВБО-11-25 Вариант 3


class CustomList(list):
    def __lt__(self, other):
        return sum(self) < sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __setitem__(self, index, value):
        previous = super().__getitem__(index)
        super().__setitem__(index, previous + value)

    def __getitem__(self, index):
        try:
            return super().__getitem__(index)
        except IndexError:
            with open("error.log", "w") as f:
                f.write(
                    f"IndexError: индекс {index} выходит за пределы списка длиной {len(self)}\n"
                )
            raise


a = CustomList([1, 2, 5, 4, 3])
b = CustomList([3, 4, 9])
print(f"a = {list(a)}, sum = {sum(a)}")
print(f"b = {list(b)}, sum = {sum(b)}")
print(f"a < b → {a < b}")
print()

a = CustomList([9, 2, 10])
b = CustomList([3, 4, 9])
print(f"a = {list(a)}, sum = {sum(a)}")
print(f"b = {list(b)}, sum = {sum(b)}")
print(f"a > b → {a > b}")
print()

c = CustomList([1, 2, 3, 4])
print(f"c = {c}")
c[2] = 5  # 3 + 5 = 8
print(f"c[2] = 5  →  {(c)}")
print()

d = CustomList([9, 2, 10])
print(f"d[0] = {d[0]}")
print(f"d[2] = {d[2]}")

try:
    temp = d[3]
except IndexError:
    print("Ошибка записана в error.log")
