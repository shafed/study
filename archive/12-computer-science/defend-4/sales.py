# импорт требуемых библиотек
import matplotlib.pyplot as plt
import numpy as np

# загрузка данных
with open("sales_27.csv", "r", encoding="utf-8") as input_file:
    # чтение заголовка данных
    # сначала читается строка, которая разбивается
    # на подстроки на сепараторе, в данном случае на запятой
    header = input_file.readline().split(",")

    # массив цен продаж
    sale_prices = []
    # массив объёма продажи
    sale_amounts = []

    # построчное чтение строк из файла
    for line in input_file:
        line = line.strip()
        if not line:
            continue

        # разбивка значений на запятой
        values = line.split(",")
        # преобразование строкового типа данных в вещественный
        values = [float(value) for value in values]
        # занесём характеристики продажи в соответствующие массивы
        sale_prices.append(values[0])
        sale_amounts.append(values[1])

# Построение гистограммы для цен продаж
plt.title("Цены продаж")
plt.xlabel("Цена продажи")
plt.hist(sale_prices, color="steelblue", edgecolor="white")
plt.tight_layout()
plt.show()

# Построение гистограммы для объёма продаж
plt.title("Объёмы продаж")
plt.xlabel("Объём продажи")
plt.hist(sale_amounts, color="steelblue", edgecolor="white")
plt.tight_layout()
plt.show()

# Построение ящика с усами для цен продаж
plt.title("Цены продаж")
plt.boxplot(sale_prices)
plt.tight_layout()
plt.show()

# Построение ящика с усами для объёма продаж
plt.title("Объёмы продаж")
plt.boxplot(sale_amounts)
plt.tight_layout()
plt.show()

# Построение точечного графика
plt.xlabel("Объём продажи")
plt.ylabel("Цена")
plt.title("Диаграмма рассеяния")
plt.scatter(x=sale_amounts, y=sale_prices, alpha=0.6, color="steelblue")
plt.tight_layout()
plt.show()
