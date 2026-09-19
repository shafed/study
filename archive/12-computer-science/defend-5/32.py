def count_control_bits(n):
    """Определяет количество контрольных битов для n информационных битов."""
    k = 1
    while (2**k) < (n + k + 1):
        k += 1
    return k


def encode(data: str) -> list[int]:
    """Кодирует сообщение кодом Хэмминга."""
    n = len(data)
    k = count_control_bits(n)
    total = n + k

    # Позиции контрольных битов (степени двойки, нумерация с 1)
    control_positions = {2**i for i in range(k)}

    # Расставляем данные на все позиции, кроме контрольных
    code = [0] * (total + 1)  # индекс 0 не используется
    data_index = 0
    for pos in range(1, total + 1):
        if pos not in control_positions:
            code[pos] = int(data[data_index])
            data_index += 1

    # Вычисляем значения контрольных битов (чётный паритет)
    for i in range(k):
        p = 2**i  # позиция контрольного бита
        ones = 0
        for pos in range(1, total + 1):
            if pos != p and (pos & p):  # позиции, проверяемые этим битом
                ones += code[pos]
        code[p] = ones % 2  # 0 если чётное, 1 если нечётное

    return code[1:]  # убираем нулевой индекс


def introduce_error(code: list[int], error_bit: int) -> list[int]:
    """Вносит ошибку в указанный бит (нумерация с 1)."""
    code = code.copy()
    code[error_bit - 1] ^= 1
    return code


def detect_and_fix(code: list[int]) -> tuple[list[int], int]:
    """
    Обнаруживает и исправляет ошибку.
    Возвращает исправленный код и позицию ошибки (0 — ошибок нет).
    """
    total = len(code)
    k = 0
    while (2**k) <= total:
        k += 1

    syndrome = 0
    for i in range(k):
        p = 2**i
        ones = 0
        for pos in range(1, total + 1):
            if pos & p:
                ones += code[pos - 1]
        if ones % 2 != 0:
            syndrome += p

    fixed = code.copy()
    if syndrome != 0:
        fixed[syndrome - 1] ^= 1

    return fixed, syndrome


def decode(code: list[int]) -> str:
    """Извлекает информационные биты из закодированного сообщения."""
    total = len(code)
    k = 0
    while (2**k) <= total:
        k += 1
    control_positions = {2**i for i in range(k)}
    return "".join(
        str(code[pos - 1])
        for pos in range(1, total + 1)
        if pos not in control_positions
    )


def print_code(label: str, code: list[int]):
    total = len(code)
    positions = list(range(1, total + 1))
    k = 0
    while (2**k) <= total:
        k += 1
    control_positions = {2**i for i in range(k)}

    header = f"{'Позиция':>10}: " + "  ".join(f"{p:2}" for p in positions)
    row = f"{'Бит':>10}: " + "  ".join(f"{b:2}" for b in code)

    markers = []
    for p in positions:
        if p in control_positions:
            markers.append(" K")
        else:
            markers.append("  ")
    mark_row = f"{'Тип':>10}: " + "  ".join(markers)

    print(f"\n{label}")
    print(header)
    print(mark_row)
    print(row)


# ─────────────────────────────────────────────
# ВАРИАНТ 27
# ─────────────────────────────────────────────
message = "0011011011001011"
error_bit = 12

print("=" * 70)
print("ВАРИАНТ 27 — КОД ХЭММИНГА")
print("=" * 70)
print(f"\nИсходное сообщение : {message}  ({len(message)} бит)")

n = len(message)
k = count_control_bits(n)
print(f"Количество контрольных битов: {k}  (2^{k} = {2**k} ≥ {n}+{k}+1 = {n + k + 1})")
print(f"Контрольные позиции: {[2**i for i in range(k)]}")
print(f"Общая длина кода: {n + k} бит")

# Кодирование
encoded = encode(message)
print_code("ЗАКОДИРОВАННОЕ СООБЩЕНИЕ:", encoded)
print(f"\n  {''.join(map(str, encoded))}")

# Внесение ошибки
with_error = introduce_error(encoded, error_bit)
print_code(f"\nСООБЩЕНИЕ С ОШИБКОЙ (бит {error_bit} инвертирован):", with_error)
print(f"\n  {''.join(map(str, with_error))}")
print(f"  {''.join(map(str, encoded))}  ← правильный")

# Обнаружение и исправление
fixed, error_pos = detect_and_fix(with_error)

print("\n" + "─" * 70)
print("ОБНАРУЖЕНИЕ ОШИБКИ — пересчёт контрольных битов:")
total = len(with_error)
k2 = 0
while (2**k2) <= total:
    k2 += 1

mismatches = []
for i in range(k2):
    p = 2**i
    # Пересчёт только по информационным позициям (без самого контрольного бита)
    ones = sum(
        with_error[pos - 1] for pos in range(1, total + 1) if (pos & p) and pos != p
    )
    received_bit = with_error[p - 1]
    calc_bit = ones % 2
    status = "✗ НЕСОВПАДЕНИЕ" if calc_bit != received_bit else "✓"
    print(f"  K{p:2}: получено={received_bit}, пересчитано={calc_bit}  {status}")
    if calc_bit != received_bit:
        mismatches.append(p)

print(f"\nНесовпавшие позиции: {mismatches}")
print(f"Позиция ошибки: {' + '.join(map(str, mismatches))} = {error_pos}")

print_code("\nИСПРАВЛЕННЫЙ КОД:", fixed)
print(f"\n  {''.join(map(str, fixed))}")

result = decode(fixed)
print("\n" + "─" * 70)
print(f"ДЕКОДИРОВАННОЕ СООБЩЕНИЕ: {result}")
print(f"ИСХОДНОЕ СООБЩЕНИЕ:       {message}")
print(f"СОВПАДАЮТ: {'✓ ДА' if result == message else '✗ НЕТ'}")
print("=" * 70)
