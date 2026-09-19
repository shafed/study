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


class ButterFly(CanFly):
    def __init__(self, high=0, speed=0) -> None:
        super().__init__(high, speed)

    def take_off(self, high=1):
        super().take_off(high)

    def fly(self, speed=0.5):
        super().fly(speed)


class Rocket(CanFly):
    def __init__(self, high=0, speed=0) -> None:
        super().__init__(high, speed)

    def take_off(self, high=500):
        super().take_off(high)
        super().fly(1000)

    def boom(self):
        print("Взорвались!")

    def land(self):
        self.high = 0
        self.speed = 0
        print("Приземлились")
        self.boom()
