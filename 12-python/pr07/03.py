class Family:
    def __init__(self, name, money, house=False) -> None:
        self.name = name
        self.money = money
        self.house = house

    def info(self):
        print(
            "Family name:",
            self.name,
            "\nFamily funds:",
            self.money,
            "\nHaving house:",
            self.house,
        )

    def earn_money(self, plus):
        self.money += plus
        print(
            f"Earned {plus} money!",
        )
        print("Current value:", self.money)

    def buy_house(self, price, discount=0):
        price_with_discount = price * (1 - discount)
        if self.money >= price_with_discount:
            self.money -= price_with_discount
            print("House purchased!")
            print("Current money:", self.money)
        else:
            print("Not enough money!")
            print("Try to buy a house again")


family = Family("Common", 100_000)
family.info()
print()
family.buy_house(900_000)
print()
family.earn_money(800_000)
print()
family.buy_house(900_000)
print()
family.info()
