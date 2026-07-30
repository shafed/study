class Car:
    def __init__(self, model) -> None:
        self.model = model

    def get_model(self):
        print("Модель автомобиля:", self.model)

    def drive(self):
        print(f"{self.model} едет")


class Truck(Car):
    def __init__(self, model, cargo=0) -> None:
        super().__init__(model)
        self.cargo = cargo

    def load(self, amount):
        self.cargo += amount
        print(f"Загрузили {amount} багажа")

    def unload(self, amount):
        if amount > self.cargo:
            print(f"В кузове только {self.cargo} груза")
        else:
            self.cargo -= amount
            print(f"Разгрузили {amount} багажа")


class PassengerCar(Car):
    def __init__(self, model, nav_model):
        super().__init__(model)
        self.nav_model = nav_model

    def activate_navigation(self):
        print(f"Навигация {self.nav_model} включена")
