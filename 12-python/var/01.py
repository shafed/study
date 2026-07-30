class BankAccount:
    def __init__(self, owner, balance=0) -> None:
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        else:
            self.balance += amount
        print(f"Текущий баланс: {self.balance}")
        self.transactions.append(f"Пополнение баланса на {amount}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if amount > self.balance:
            raise ValueError("Недостаточно средств")
        else:
            self.balance -= amount
        print(f"Текущий баланс: {self.balance}")
        self.transactions.append(f"Списание с баланса на {amount}")

    def get_history(self):
        for i in self.transactions:
            print(i)

    def __str__(self) -> str:
        return f"Владелец: {self.owner} | Баланс: {self.balance}"


account = BankAccount("Иван", 1000)
print(account)
