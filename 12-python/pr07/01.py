class Monitors:
    def __init__(self, frequency):
        self.model = "Nvidia"
        self.matrix = "IPS"
        self.resolution = "4K"
        self.frequency = frequency


class Headphones:
    def __init__(self, sensitivity, microphone):
        self.model = "HyperX"
        self.sensitivity = sensitivity
        self.microphone = microphone


monitor1 = Monitors(240)
monitor1 = Monitors(144)
monitor1 = Monitors(60)

heaphones1 = Headphones(100, True)
heaphones1 = Headphones(120, False)
heaphones1 = Headphones(80, True)
