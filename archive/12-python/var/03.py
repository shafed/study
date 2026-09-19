from abc import ABC, abstractmethod
from math import pi


class Shape(ABC):
    def __init__(self, color) -> None:
        self.color = color

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

    def describe(self):
        print(
            f"Фигура: {type(self).__name__} | Цвет: {self.color} | Площадь: {self.area()} | Периметр: {self.perimeter()}"
        )


class Circle(Shape):
    def __init__(self, color, radius) -> None:
        super().__init__(color)
        self.radius = radius

    def area(self):
        return pi * self.radius**2

    def perimeter(self):
        return 2 * pi * self.radius


class Rectangle(Shape):
    def __init__(self, color, width, height) -> None:
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Square(Rectangle):
    def __init__(self, color, side) -> None:
        super().__init__(color, side, side)


c = Circle("красный", 5)
r = Rectangle("синий", 4, 6)
s = Square("зелёный", 7)

c.describe()
# Фигура: Circle | Цвет: красный | Площадь: 78.54 | Периметр: 31.42

r.describe()
# Фигура: Rectangle | Цвет: синий | Площадь: 24.00 | Периметр: 20.00
