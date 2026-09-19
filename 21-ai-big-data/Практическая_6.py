# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] colab_type="text" id="view-in-github"
# <a href="https://colab.research.google.com/github/shafed/study/blob/main/%D0%9F%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_6.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# %% [markdown] id="c0000"
# # Практическая работа 6. Подготовка набора данных
#
# Это **первый отчётный ноутбук** курса. Он закрывает практики **1–5**. Второй отчёт (практика 16) будет по практикам 7–15.
#
# **Предметная задача.** IT-компания ведёт журнал обращений в службу поддержки (service desk): сбои продуктов, нагрузка на серверы, эскалации. По этим данным позже можно учить модель, которая заранее замечает **нарушение SLA** (`sla_breached`: 1 — срок ответа сорван, 0 — уложились). В этой работе модель **не строится**. Нужно осмотреть, посчитать, нарисовать и привести таблицу в порядок — как на практиках 1–5.
#
# Официальная формулировка занятия: загрузка → разведочный анализ и визуализация → предобработка → конструирование признаков. У нас те же шаги разложены на **пять блоков**, по одной пройденной практике.
#
# ---
#
# ### Что входит в работу (15 баллов)
#
# | Блок | Практика | Что сдаёте | Баллы |
# |------|----------|------------|------:|
# | 1 | Основы pandas | код осмотра, выборки и нового столбца + вопросы | 3 |
# | 2 | NumPy | код на массивах (срез, маска, broadcasting) + вопросы | 3 |
# | 3 | Группировка | `groupby`, `pivot_table`, дата из Unix + вопросы | 3 |
# | 4 | Визуализация | не меньше 4 графиков разных типов и выводы | 3 |
# | 5 | Подготовка данных | пропуски, текст, кодирование, масштаб, новые признаки + вопросы | 3 |
# | | | **Итого** | **15** |
#
# Код без запуска и пустые ответы на вопросы не засчитываются. Числа и графики у каждого свои: датасет строится из вашего ФИО и номера в списке.
#
# ---
#
# ### Важно: у каждого студента свой набор данных
#
# Данные **не скачиваются с Kaggle**. Они генерируются из персонального `SEED`. Заполните ячейку с фамилией, прежде чем запускать остальные.

# %% [markdown] id="c0001"
# ## Шаг 0. Персонализация (обязательно)
#
# Впишите **фамилию, имя** и **номер по списку группы**. Из них считается `SEED` — зерно генератора, которое задаёт ваш вариант.

# %% id="c0002"
# ==========================================================
# ⬇️  ЗАПОЛНИТЕ ЭТИ ТРИ ПОЛЯ СВОИМИ ДАННЫМИ
# ==========================================================
last_name   = "Шапаренко"    # <-- впишите свою фамилию
first_name  = "Фёдор"      # <-- впишите своё имя
list_number = 27           # <-- ваш номер по списку (целое число)
# ==========================================================

import hashlib

def make_seed(last: str, first: str, number: int) -> int:
    # ФИО + номер -> стабильный seed 0..99999
    key = f"{last.strip().lower()}|{first.strip().lower()}|{int(number)}"
    return int(hashlib.sha256(key.encode("utf-8")).hexdigest(), 16) % 100_000

SEED = make_seed(last_name, first_name, list_number)

print("Студент:", last_name, first_name, f"(№{list_number})")
print("Ваш персональный SEED:", SEED)
print("Запишите SEED в итоговый отчёт — он подтверждает вариант.")

# %% [markdown] id="c0003"
# > **Как это работает.** `hashlib.sha256` переводит строку с ФИО и номером в большое число, затем берётся остаток от деления на 100 000. Одинаковые ФИО и номер всегда дают один и тот же SEED, разные — почти всегда разный. Весь датасет ниже зависит только от этого числа.

# %% [markdown] id="c0004"
# ## Подготовка окружения
#
# В Google Colab пакеты уже есть. Локально при необходимости: `pip install pandas numpy matplotlib seaborn`.

# %% id="c0005"
# %matplotlib inline

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", 50)
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (8, 4)


# %% [markdown] id="c0006"
# ## Генерация вашего набора данных
#
# Ячейка ниже создаёт **ваш** журнал обращений IT-службы. Разбирать генератор не нужно — достаточно запустить.
#
# Внутри специально заложены пропуски, выбросы, дубликаты и разный регистр текста, иначе предобработка была бы формальной.
#
# **Признаки**
#
# | Столбец | Смысл |
# |---------|-------|
# | `ticket_id` | идентификатор обращения |
# | `opened_ts` | время открытия в Unix-секундах |
# | `department` | отдел: Support, Backend, DevOps, Security, Data |
# | `product` | продукт: Cloud, CRM, Billing, Auth, Analytics |
# | `priority` | приоритет: Low, Medium, High, Critical |
# | `channel` | канал: Email, Slack, Portal, Phone |
# | `assignee_level` | уровень исполнителя: Junior, Middle, Senior |
# | `client_tier` | тариф клиента: Free, Pro, Enterprise |
# | `cpu_pct` | загрузка CPU на затронутом узле, % |
# | `memory_mb` | занятая память, МБ |
# | `n_reopens` | сколько раз тикет открывали повторно |
# | `comments` | число комментариев в тикете |
# | `resolve_hours` | часы до закрытия |
# | **`sla_breached`** | **цель**: 1 — SLA нарушен, 0 — нет |

# %% id="c0008"
#@title Создание персонального датасета (нажмите ▶️) { display-mode: "form" }

def load_it_tickets(seed: int, n: int = 1800) -> "pd.DataFrame":
    """Индивидуальный «грязный» журнал IT-обращений по seed."""
    rng = np.random.default_rng(seed)

    opened_ts = rng.integers(1_735_689_600, 1_751_241_600, size=n)
    department = rng.choice(
        ["Support", "Backend", "DevOps", "Security", "Data"],
        size=n, p=[0.32, 0.22, 0.18, 0.14, 0.14],
    )
    product = rng.choice(
        ["Cloud", "CRM", "Billing", "Auth", "Analytics"], size=n
    )
    priority = rng.choice(
        ["Low", "Medium", "High", "Critical"], size=n, p=[0.40, 0.30, 0.20, 0.10]
    )
    channel = rng.choice(["Email", "Slack", "Portal", "Phone"], size=n)
    assignee = rng.choice(["Junior", "Middle", "Senior"], size=n, p=[0.35, 0.45, 0.20])
    tier = rng.choice(["Free", "Pro", "Enterprise"], size=n, p=[0.45, 0.40, 0.15])
    cpu_pct = np.clip(np.round(rng.normal(48, 18, size=n), 1), 1, 99)
    memory_mb = np.clip(np.round(rng.normal(2200, 850, size=n), 0), 256, None)
    n_reopens = rng.poisson(0.7, size=n)
    comments = rng.poisson(4.0, size=n) + 1
    resolve_hours = np.clip(np.round(rng.lognormal(1.55, 0.75, size=n), 2), 0.2, 240)

    logit = (
        -1.4
        + 1.4 * (priority == "Critical")
        + 0.7 * (priority == "High")
        - 0.4 * (priority == "Low")
        + 0.035 * resolve_hours
        + 0.018 * cpu_pct
        + 0.55 * (department == "Security")
        + 0.35 * (n_reopens >= 2)
        - 0.45 * (assignee == "Senior")
        - 0.30 * (tier == "Enterprise")
    )
    sla = (rng.uniform(size=n) < 1 / (1 + np.exp(-logit))).astype(int)

    df = pd.DataFrame({
        "ticket_id": np.arange(10_000, 10_000 + n),
        "opened_ts": opened_ts,
        "department": department,
        "product": product,
        "priority": priority,
        "channel": channel,
        "assignee_level": assignee,
        "client_tier": tier,
        "cpu_pct": cpu_pct,
        "memory_mb": memory_mb,
        "n_reopens": n_reopens,
        "comments": comments,
        "resolve_hours": resolve_hours,
        "sla_breached": sla,
    })

    df.loc[rng.choice(n, int(0.06 * n), replace=False), "resolve_hours"] = np.nan
    df.loc[rng.choice(n, int(0.04 * n), replace=False), "cpu_pct"] = np.nan
    df.loc[rng.choice(n, int(0.03 * n), replace=False), "comments"] = np.nan
    df.loc[rng.choice(n, 10, replace=False), "resolve_hours"] *= 9
    df.loc[rng.choice(n, 8, replace=False), "memory_mb"] *= 7
    ridx = rng.choice(n, int(0.12 * n), replace=False)
    df.loc[ridx, "department"] = df.loc[ridx, "department"].str.upper()
    pidx = rng.choice(n, int(0.08 * n), replace=False)
    df.loc[pidx, "product"] = "  " + df.loc[pidx, "product"].str.lower() + " "
    df = pd.concat([df, df.sample(int(0.025 * n), random_state=seed)], ignore_index=True)
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)

print("Функция load_it_tickets готова.")

# %% [markdown] id="c0009"
# Загрузите **ваш** набор одной строкой:

# %% id="c0010"
df_raw = load_it_tickets(SEED)

print("Ваш датасет создан. Размер:", df_raw.shape)
print("Доля нарушений SLA:", f"{df_raw['sla_breached'].mean():.1%}")

# %% [markdown] id="c0011"
# > В таблице уже спрятаны пропуски, выбросы, дубликаты и неаккуратный текст. Найти и поправить их — часть заданий. Дальше везде работайте со **своим** `df_raw`, если в блоке не сказано иное.

# %% [markdown] id="c0012"
# ---
# # Этап 1. Основы pandas (практика 1)
#
# **Цель.** Убедиться, что таблица загрузилась, понять размер и типы, выбрать строки и столбцы, добавить признак, сохранить фрагмент.
#
# ### Пример
#
# Стандартный осмотр и простая выборка. Запустите ячейки — те же команды понадобятся в задании.

# %% id="c0013"
print("Размер (строки, столбцы):", df_raw.shape)
print("Имена столбцов:", list(df_raw.columns))
print("\nПервые 5 строк:")
display(df_raw.head())
print("\nТипы и непропуски:")
df_raw.info()

# %% id="c0014"
# loc — по подписям, iloc — по номерам
print("Один столбец (первые значения priority):")
print(df_raw["priority"].head())
print("\nДве строки и три столбца через loc:")
display(df_raw.loc[0:1, ["ticket_id", "department", "priority"]])
print("Критические тикеты:", (df_raw["priority"] == "Critical").sum())

# %% [markdown] id="c0015"
# ### Задание 1
#
# В ячейках ниже, **на своих данных**:
#
# 1. Выведите **последние 8 строк** (`.tail(8)`).
# 2. Посчитайте **число полных дубликатов** (`.duplicated().sum()`).
# 3. Через `.loc` отберите тикеты с `priority` равным `"High"` **или** `"Critical"` и столбцы `ticket_id`, `department`, `priority`, `resolve_hours`. Сколько таких строк?
# 4. Добавьте столбец `is_slow`: `True`, если `resolve_hours` больше 24 (пропуски пусть останутся пропусками). Затем **переименуйте** `n_reopens` в `reopen_count`.
# 5. Сохраните первые 100 строк текущего `df_raw` в файл `it_tickets_head.csv`.

# %% id="c0016"
# ▼▼▼ ВАШ КОД (Задание 1) ▼▼▼

# 1. Последние 8 строк
print(df_raw.tail(8))


# %% id="c0017"
# 2. Число дубликатов
df_raw.duplicated().sum()

# %% id="c0018"
# 3. High или Critical, выбранные столбцы
a = df_raw.loc[(df_raw["priority"] == "High") | (df_raw["priority"] == "Critical"),
["ticket_id", "department", "priority", "resolve_hours"]]
len(a)

# %% id="c0019"
# 4. Столбец is_slow и переименование n_reopens → reopen_count
df_raw["is_slow"] = (df_raw["resolve_hours"] >
                     24).where(df_raw["resolve_hours"].notna())
df_raw = df_raw.rename(columns={"n_reopens": "reopen_count"})

# %% id="c0020"
# 5. Сохранение it_tickets_head.csv
df_raw.head(100).to_csv("it_tickets_head.csv", index=False)

# ▲▲▲ КОНЕЦ ВАШЕГО КОДА ▲▲▲

# %% [markdown] id="c0021"
# **Контрольные вопросы к этапу 1** (ответьте текстом):
#
# 1. Чем `.info()` отличается от `.describe()`? Что показывает каждый?
# 2. Когда удобнее `.loc`, а когда `.iloc`?
# 3. Почему дубликаты строк могут испортить и статистику, и будущую модель?

# %% [markdown] id="c0022"
# *Ответы (двойной клик):*
#
# 1. `.info()` показывает структуру таблицы: типы столбцов, число не пустых
#    ячеек, и в конце память; а `.describe()` - статистику столбцов:
#    среднее, разброс, минимум, максимум, квартили
#
# 2. `.loc` удобен, когда знаем названия столбцов и строк или когда нужна
#    маска для них, а `.iloc` - когда нужно вывести первые `n` строк или
#    `k`-ый столбец
#
# 3. потому что статистика будет иметь другие значения; копия может попасть в
#    тренировочную и тестовую выборки

# %% [markdown] id="c0023"
# ---
# # Этап 2. NumPy
#
# **Цель.** Перевести столбец в массив, посчитать агрегаты без цикла `for`, срезать, отфильтровать маской, сделать поэлементную операцию (broadcasting).
#
# Таблица удобна, когда у столбцов есть имена. Массив удобен, когда нужно быстро посчитать «все значения сразу».

# %% [markdown] id="c0025"
# ### Пример

# %% id="c0026"
cpu = df_raw["cpu_pct"].to_numpy(dtype=float)
print("Тип:", type(cpu), "форма:", cpu.shape, "dtype:", cpu.dtype)
print("Первые 8 значений:", cpu[:8])
print("Среднее без учёта NaN:", np.nanmean(cpu))
print("Максимум:", np.nanmax(cpu))

# маска: загрузка выше 80% (NaN даст False)
high_cpu = cpu > 80
print("Доля наблюдений с CPU > 80%:", np.nanmean(high_cpu))

# broadcasting: перевод % в долю 0..1
cpu_share = cpu / 100
print("Доля CPU, первые 5:", cpu_share[:5])

# %% [markdown] id="c0027"
# ### Задание 2
#
# Работайте с массивами, не с циклами `for` по строкам.
#
# 1. Соберите массивы `hours` из `resolve_hours` и `mem` из `memory_mb` (тип `float`).
# 2. Посчитайте **медиану** и **стандартное отклонение** `hours`, игнорируя NaN.
# 3. Срезом возьмите **последние 15** значений `mem`.
# 4. Постройте маску «память выше 4000 МБ» и выведите, **сколько** таких тикетов (для NaN считайте «не выше»).
# 5. Сделайте z-оценку памяти через broadcasting: `(mem - mean) / std`, где mean и std без NaN. Выведите 5 первых z-оценок.

# %% id="c0028"
# ▼▼▼ ВАШ КОД (Задание 2) ▼▼▼

# 1. Массивы hours и mem

# %% id="c0029"
# 2. Медиана и std для hours

# %% id="c0030"
# 3. Срез последних 15 значений mem

# %% id="c0031"
# 4. Маска памяти > 4000

# %% id="c0032"
# 5. Z-оценка памяти

# ▲▲▲ КОНЕЦ ВАШЕГО КОДА ▲▲▲

# %% [markdown] id="c0033"
# **Контрольные вопросы к этапу 2:**
#
# 1. Чем массив NumPy принципиально отличается от списка Python?
# 2. Что такое broadcasting? Приведите пример из этого задания.
# 3. Почему для среднего по столбцу с пропусками нужен `np.nanmean`, а не `np.mean`?

# %% [markdown] id="c0034"
# *Ответы:*
#
# 1.
#
# 2.
#
# 3.

# %% [markdown] id="c0035"
# ---
# # Этап 3. Агрегирование и группировка (практика 3)
#
# **Цель.** Ответить на вопросы вида «какая доля нарушений SLA **в каждом** отделе?» без ручного фильтра. Схема одна: разбить → посчитать → собрать.
#
# Unix-время `opened_ts` нужно превратить в обычную дату, иначе группировка по дням невозможна.

# %% [markdown] id="c0037"
# ### Пример

# %% id="c0038"
print("Среднее время решения по приоритету:")
display(
    df_raw.groupby("priority")["resolve_hours"].agg(["count", "mean", "median"]).round(2)
)

print("\nСводная: доля нарушений SLA по отделу и уровню исполнителя")
pivot = pd.pivot_table(
    df_raw, values="sla_breached", index="department",
    columns="assignee_level", aggfunc="mean",
)
display(pivot.round(3))

# %% id="c0039"
df_time = df_raw.copy()
df_time["opened_at"] = pd.to_datetime(df_time["opened_ts"], unit="s")
print("Минимум и максимум даты:", df_time["opened_at"].min(), df_time["opened_at"].max())
print("Тикетов по месяцам:")
print(df_time.groupby(df_time["opened_at"].dt.to_period("M")).size())

# %% [markdown] id="c0040"
# ### Задание 3 (2 балла за код + 1 балл за вопросы)
#
# 1. Сделайте `groupby` по `product`: для каждого продукта — число тикетов, среднее `cpu_pct`, доля `sla_breached`. Отсортируйте по доле нарушений **по убыванию**.
# 2. Постройте `pivot_table`: строки — `channel`, столбцы — `priority`, значения — среднее `resolve_hours`.
# 3. Переведите `opened_ts` в datetime. Добавьте столбец `opened_date` (только дата). Посчитайте число тикетов **по дням** и выведите 5 дней с наибольшим числом обращений.
# 4. Дополнительно: `groupby` по `client_tier` с `.agg` сразу по нескольким столбцам — среднее `resolve_hours` и сумма `sla_breached`.

# %% id="c0041"
# ▼▼▼ ВАШ КОД (Задание 3) ▼▼▼

# 1. groupby по product

# %% id="c0042"
# 2. pivot_table channel × priority

# %% id="c0043"
# 3. Дата из Unix и топ-5 дней

# %% id="c0044"
# 4. Несколько агрегатов по client_tier

# ▲▲▲ КОНЕЦ ВАШЕГО КОДА ▲▲▲

# %% [markdown] id="c0045"
# **Контрольные вопросы к этапу 3:**
#
# 1. Чем `groupby` отличается от `pivot_table`? Когда что удобнее?
# 2. Что делает `agg` со словарём нескольких функций?
# 3. Почему Unix-секунды нельзя сразу группировать «по месяцу», не переводя в datetime?

# %% [markdown] id="c0046"
# *Ответы:*
#
# 1.
#
# 2.
#
# 3.

# %% [markdown] id="c0047"
# ---
# # Этап 4. Визуализация (практика 4) — 3 балла
#
# **Цель.** Увидеть форму распределения, выброс, связь признаков с `sla_breached`. Таблица среднее не покажет: одинаковое среднее бывает при разной форме гистограммы.
#
# Подписывайте оси и заголовок (`plt.title("Рис. N. ...")`).

# %% [markdown] id="c0049"
# ### Пример

# %% id="c0050"
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
df_raw["sla_breached"].value_counts().sort_index().plot(
    kind="bar", ax=axes[0], color=["#4C9F70", "#D9534F"]
)
axes[0].set_title("Рис. 1. Баланс классов: нарушение SLA")
axes[0].set_xticklabels(["уложились", "сорвали"], rotation=0)
axes[0].set_ylabel("Число тикетов")

sns.histplot(df_raw["cpu_pct"].dropna(), bins=30, ax=axes[1], color="steelblue")
axes[1].set_title("Рис. 2. Распределение загрузки CPU")
plt.tight_layout()
plt.show()

# %% id="c0051"
plt.figure(figsize=(8, 4))
sns.boxplot(data=df_raw, x="priority", y="resolve_hours",
            order=["Low", "Medium", "High", "Critical"])
plt.title("Рис. 3. Время решения по приоритету")
plt.ylabel("часы")
plt.show()

# %% [markdown] id="c0052"
# ### Задание 4
#
# Постройте **не меньше четырёх разных типов** графиков по **своим** данным. Обязательно:
#
# 1. **Гистограмма** `resolve_hours` (видно ли выбросы справа?).
# 2. **Boxplot** `cpu_pct` в разрезе `sla_breached`.
# 3. **Тепловая карта** корреляций числовых столбцов (`corr(numeric_only=True)` + `sns.heatmap(..., annot=True)`).
# 4. **Столбчатая или круговая** диаграмма: доля нарушений SLA по `department` **или** по `product`.
# 5. По желанию пятый график (scatter `cpu_pct` vs `memory_mb`, stacked bar канала и SLA и т. п.).
#
# После графиков напишите 2–3 вывода **по вашему SEED**, не общие фразы из учебника.

# %% id="c0053"
# ▼▼▼ ВАШ КОД (Задание 4) ▼▼▼

# График 1: гистограмма resolve_hours

# %% id="c0054"
# График 2: boxplot cpu_pct по sla_breached

# %% id="c0055"
# График 3: тепловая карта корреляций

# %% id="c0056"
# График 4: доля SLA по отделу или продукту

# %% id="c0057"
# График 5 (по желанию)

# ▲▲▲ КОНЕЦ ВАШЕГО КОДА ▲▲▲

# %% [markdown] id="c0058"
# **Выводы по графикам** (2–3 закономерности из ВАШИХ данных):
#
# 1.
#
# 2.
#
# 3.

# %% [markdown] id="c0059"
# **Контрольные вопросы к этапу 4:**
#
# 1. Что показывает boxplot и как по нему увидеть выброс?
# 2. Корреляция и причинно-следственная связь — в чём разница? Пример из IT-журнала.
# 3. Почему при редких нарушениях SLA одной accuracy на будущей модели может не хватить?

# %% [markdown] id="c0060"
# *Ответы:*
#
# 1.
#
# 2.
#
# 3.

# %% [markdown] id="c0061"
# ---
# # Этап 5. Подготовка данных и признаки (практика 5)
#
# **Цель.** Убрать дубликаты, закрыть пропуски, привести текст к одному виду, закодировать категории, масштабировать числа, собрать несколько новых признаков. Это тот же конвейер, что на практике 5, только на вашем журнале тикетов.
#
# Работайте с копией: исходный `df_raw` не затирайте.

# %% [markdown] id="c0062"
# ### Пример

# %% id="c0063"
df = df_raw.copy()
before = df.shape[0]
df = df.drop_duplicates().reset_index(drop=True)
print("Удалено дубликатов:", before - df.shape[0])
print("Пропуски по столбцам:")
print(df.isna().sum())

median_cpu = df["cpu_pct"].median()
df["cpu_pct"] = df["cpu_pct"].fillna(median_cpu)
print("Пропусков в cpu_pct после заполнения:", int(df["cpu_pct"].isna().sum()))

# %% id="c0064"
# Текст: пробелы и регистр. Без этого Backend и BACKEND — разные категории.
demo = df["department"].astype(str).str.strip().str.title()
print("Уникальные отделы до:", df["department"].nunique())
print("После strip+title:", demo.nunique())
print(sorted(demo.unique()))

# %% [markdown] id="c0065"
# ### Задание 5
#
# Начните заново с копии `df_raw`. Сохраните результат в `df_clean`, матрицу признаков в `X`, цель в `y`.
#
# 1. Удалите дубликаты.
# 2. Заполните пропуски: `resolve_hours` и `cpu_pct` — **медианой**, `comments` — **медианой** или нулём. Проверьте, что пропусков не осталось.
# 3. Приведите `department` и `product` к одному виду: `.str.strip()` и единый регистр (например `.str.title()`). Снова посчитайте число уникальных значений.
# 4. Закодируйте категории `department`, `product`, `priority`, `channel`, `assignee_level`, `client_tier` через `pd.get_dummies(...)`.
# 5. Создайте **не меньше трёх** осмысленных признаков, например:
#    - `is_critical` — флаг приоритета Critical;
#    - `load_score` — `cpu_pct * memory_mb / 1000`;
#    - `reopen_rate` — `n_reopens / comments` (защититесь от деления на ноль);
#    - свой признак (выходной ли день из `opened_ts`, «долгий тикет» и т. п.).
# 6. Отберите числовые столбцы (без `ticket_id` и `opened_ts`) и масштабируйте их `StandardScaler`. Сложите с dummy-признаками в `df_clean`.
# 7. Соберите `X` (всё, кроме `sla_breached` и идентификаторов) и `y = df_clean["sla_breached"]`. Напечатайте формы.

# %% id="c0066"
# ▼▼▼ ВАШ КОД (Задание 5) ▼▼▼
from sklearn.preprocessing import StandardScaler

df = df_raw.copy()

# 1–2. Дубликаты и пропуски

# %% id="c0067"
# 3. Текст department и product

# %% id="c0068"
# 4. get_dummies

# %% id="c0069"
# 5. Новые признаки (минимум 3, один — свой)

# %% id="c0070"
# 6–7. Масштаб, df_clean, X, y
df_clean = None
X = None
y = None

# print("Размер X:", X.shape, "| Размер y:", y.shape)

# ▲▲▲ КОНЕЦ ВАШЕГО КОДА ▲▲▲

# %% [markdown] id="c0071"
# **Контрольные вопросы к этапу 5:**
#
# 1. Когда для пропусков берут медиану, а когда среднее?
# 2. Что такое One-Hot (`get_dummies`) и почему отделы нельзя просто заменить числами 1, 2, 3…?
# 3. Зачем масштабировать признаки перед линейными моделями и kNN и почему дереву это обычно не нужно?
# 4. Почему `ticket_id` нельзя подавать в модель как обычный признак?

# %% [markdown] id="c0072"
# *Ответы:*
#
# 1.
#
# 2.
#
# 3.
#
# 4.

# %% [markdown] id="c0073"
# ---
# # Итоговый отчёт студента
#
# Заполните по **вашему** варианту. Это обязательная часть (без отчёта работа не принимается).

# %% [markdown] id="c0074"
# ### Данные варианта
#
# | Поле | Значение |
# |------|----------|
# | ФИО |  |
# | Номер по списку |  |
# | Персональный SEED |  |
# | Строк в `df_raw` |  |
# | Строк после удаления дубликатов |  |
# | Доля `sla_breached` |  |
# | Размер `X` (строки × столбцы) |  |
#
# ### Кратко по этапам
#
# 1. Что необычного увидели при осмотре (типы, дубликаты, пропуски)?
# 2. Какой отдел / продукт / приоритет чаще ломает SLA на ваших графиках?
# 3. Какие три новых признака сделали и зачем?

# %% [markdown] id="c0075"
# ### Финальная самопроверка
#
# Ячейка ниже не ставит оценку, а подсказывает, какие переменные ещё не созданы.

# %% id="c0076"
problems = []

if "SEED" not in dir():
    problems.append("Не вычислен SEED (шаг 0).")
if "df_raw" not in dir():
    problems.append("Не создан df_raw (генерация датасета).")
if "df_clean" not in dir() or df_clean is None:
    problems.append("Не создан df_clean (этап 5).")
if "X" not in dir() or X is None:
    problems.append("Не создана матрица X (этап 5).")
if "y" not in dir() or y is None:
    problems.append("Не создан вектор y (этап 5).")
if "df_clean" in dir() and df_clean is not None:
    n_na = int(df_clean.isna().sum().sum())
    if n_na > 0:
        problems.append(f"В df_clean ещё есть пропуски: {n_na}.")

if problems:
    print("Ещё не готово:")
    for item in problems:
        print(" -", item)
else:
    print("Базовые переменные на месте. Проверьте текстовые ответы и отчёт.")
    print("SEED:", SEED, "| X:", X.shape, "| y:", y.shape)

# %% [markdown] id="c0077"
# ---
# ### Как сдать работу
#
# 1. Запустите все ячейки **сверху вниз** без ошибок (`Среда выполнения → Перезапустить и выполнить всё`).
# 2. Заполните код заданий, контрольные вопросы и итоговый отчёт.
# 3. Сохраните файл: `Файл → Скачать → Скачать .ipynb`.
# 4. Переименуйте в `Фамилия_Имя_ПР6.ipynb` и загрузите в Moodle.
#
# Повторно напомню шкалу: 5 блоков × 3 балла = **15 баллов**. Пустой шаблон без запуска не оценивается.
