class Primes:
    def __init__(self, number: int) -> None:
        self.number = number
        self.current = 2

    def __iter__(self) -> object:
        return self

    def __next__(self):
        while self.current <= self.number:
            if self.is_prime(self.current):
                prime = self.current
                self.current += 1
                return prime
            self.current += 1
        raise StopIteration

    def is_prime(self, number):
        if number < 2:
            return False
        for i in range(2, int(number**0.5) + 1):
            if number % i == 0:
                return False
        return True


N = int(input())
prime_nums = Primes(N)
for elem in prime_nums:
    print(elem, end=" ")
