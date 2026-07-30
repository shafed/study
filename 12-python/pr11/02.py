class File:
    def __init__(self, name, mode) -> None:
        self.name = name
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.name, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()


with File("test.txt", "w") as f:
    f.write("Привет, это проверка класса File!")
