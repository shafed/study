# 3. У вас есть файл server_logs.txt с записями о посещениях веб-сервера. Каждая строка содержит: IP-адрес, дату, HTTP-метод, запрошенный URL и код ответа. Необходимо получить словарь, отфильтровать успешные запросы (коды 200-299), найти все уникальные адреса и подсчитать кол-во запросов от каждого уникального адреса (желательно с помощью reduce).
# https://docs.google.com/document/d/1XZXEQkyEAsjJAt4RaOwyoVRmwi4hjwuLbU_li99AZLQ/edit?usp=sharing – тестовый набор для 3 задачи
# example: 192.168.0.1 2026-03-10 GET /index.html 300
from functools import reduce

with open("server_logs.txt", "r") as file:
    requests = [i.split() for i in file.readlines()]  # splitting every line
    d = reduce(
        # iteratively update dictionary with +1 count unique IP
        lambda acc, item: {**acc, item[0]: acc.get(item[0], 0) + 1},
        # filter successful request
        filter(lambda x: 200 <= int(x[4]) <= 299, requests),
        {},
    )
    d = {}
    for item in requests:
        if 200 <= int(item[4]) <= 299:
            d[item[0]] = d.get(item[0], 0) + 1
    print("dict:", d)
