class Robot:
    def __init__(self, model) -> None:
        self.model = model
        print("Я - робот")


class CanFly:
    def __init__(self, high=0, speed=0) -> None:
        self.high = high
        self.speed = speed

    def take_off(self, high):
        self.high = high
        print(f"Взлетели. Высота {self.high}")

    def fly(self, speed):
        self.speed = speed
        print(f"Летим на высота {self.high}, скорость {self.speed}")

    def land(self):
        self.high = 0
        self.speed = 0
        print("Приземлились, высота 0, скорость 0")

    def get_info(self):
        print(f"Скорость {self.speed}, высота {self.high}")


class FlyingRobot(Robot, CanFly):
    def __init__(self, model) -> None:
        Robot.__init__(self, model)
        CanFly.__init__(self)


class Dron(FlyingRobot):
    def __init__(self, model, position=0) -> None:
        super().__init__(model)
        self.position = position

    def operate(self):
        self.position += 10
        print("Веду разведку с воздуха")


class WarRobot(FlyingRobot):
    def __init__(self, model, weapon) -> None:
        super().__init__(model)
        self.weapon = weapon

    def operate(self):
        print(f"Защита военного объекта с воздуха через {self.weapon}")
