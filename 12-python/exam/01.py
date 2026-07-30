n = int(input())
s = "На лугу пасётся "

if 11 <= n % 100 <= 14:
    s += f"{n} коней"
elif n % 10 == 1:
    s += f"{n} конь"
elif 1 < n % 10 <= 4:
    s += f"{n} коня"
elif 5 <= n % 10 <= 9 or n % 10 == 0:
    s += f"{n} коней"

print(s)
