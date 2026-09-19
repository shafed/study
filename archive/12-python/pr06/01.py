# 1. Есть списки студентов и оценок, содержащие в себе фамилии/имена студентов и оценки по n-ым дисциплинам. Получить список кортежей студентов (фамилия/имя, средний бал), средний балл которых >= 4. Необходимо реализовать задачу, используя знания о функциях высшего порядка.

import random

students = ["Artem", "Edmon", "Sanya", "Fedos", "Shuropovert"]
n = int(input())
marks = [[random.randint(2, 5) for _ in range(n)] for _ in range(len(students))]
avg = list(map(lambda s, i: (s, sum(i) / n), students, marks))
res = list(filter(lambda x: x[1] >= 4, avg))
print(*res)
