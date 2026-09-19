class Student:
    def __init__(self, name, gpa):
        self.name = name
        self.gpa = gpa

    def __str__(self):
        return f"Студент: {self.name} | GPA: {self.gpa:.2f}"


def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and key.gpa > arr[j].gpa:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


students = [
    Student("Иван", 4.5),
    Student("Мария", 3.8),
    Student("Пётр", 4.9),
]

insertion_sort(students)
for i in students:
    print(i)
