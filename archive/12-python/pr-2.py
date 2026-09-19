# 27 mod 12 = 3
# Шапаренко Фёдор КВБО-11-25
from abc import ABC, abstractmethod
from random import randint


class Figure(ABC):
    @abstractmethod
    def perimeter(self):
        return

    @abstractmethod
    def area(self):
        pass

    def __str__(self) -> str:
        return f"Периметр: {self.perimeter()} | Площадь: {self.area()}"


class Square(Figure):
    def __init__(self, side) -> None:
        self.side = side

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, value):
        if value > 0:
            self._side = value
        else:
            raise ValueError("Сторона должна быть > 0")

    def perimeter(self):
        return 4 * self.side

    def area(self):
        return self.side * self.side

    def __gt__(self, other):
        return self.perimeter() > other.perimeter()


# bad = Square(0)
squares = [Square(randint(5, 20)) for _ in range(randint(3, 10))]

print(
    f"Сравнение периметров {squares[0].perimeter()} > {squares[1].perimeter()}: {squares[0] > squares[1]}\n"
)

squares.sort()
print("Отсортированные квадраты:")
for one in squares:
    print(one)
