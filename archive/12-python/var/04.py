from functools import reduce


class Product:
    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price

    def __str__(self):
        return f"{self.name} | {self.category} | {self.price:.2f}₽"


products = [
    Product("Ноутбук", "Электроника", 75000),
    Product("Мышь", "Электроника", 800),
    Product("Телефон", "Электроника", 55000),
    Product("Стол", "Мебель", 12000),
    Product("Стул", "Мебель", 900),
    Product("Наушники", "Электроника", 3500),
]

filtered = filter(lambda x: x.price > 1000, products)
filtered_with_discount = map(lambda x: x.price * 0.85, filtered)
summary_prices = reduce(lambda x, y: x + y, filtered_with_discount)
print(summary_prices)


def apply_discount(products, discount_fn):
    return list(map(discount_fn, products))


discount_15 = lambda x: Product(x.name, x.category, x.price * 0.85)
discount_vip = lambda x: Product(x.name, x.category, x.price * 0.70)

print("-----")
print(*apply_discount(products, discount_15), sep="\n")
print("-----")
print(*apply_discount(products, discount_vip), sep="\n")
