from abc import ABC, abstractmethod


class Transport(ABC):
    def __init__(self, color, speed) -> None:
        self.color = color
        self.speed = speed

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def bip(self):
        pass


class Music:
    def play_music(self):
        print("Играем музыку")

    def stop_music(self):
        print("Останавливаем музыку")


class Car(Transport):
    def move(self):
        print(f"Машина двигается по земле со скоростью {self.speed}")

    def bip(self):
        print("Биип!")


class Boat(Transport):
    def move(self):
        print(f"Лодка двигается по воде со скоростью {self.speed}")

    def bip(self):
        print("Сигнал")


class Amphibia(Music, Transport):
    def move(self):
        print(f"Амфибия двигается по земле со скоростью {self.speed}")

    def move_water(self):
        print(f"Амфибия двигается по воде со скоростью {self.speed}")

    def bip(self):
        print("Сигнал")
