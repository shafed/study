// Шапаренко Фёдор Александрович
// КВБО-11-25
// Вариант 27

// 2. Вычисление выражений с выводом на экран
x = log(8)/log(5) + 0.7*sin(0.5);
y = 3*cos(%pi/2) + sin(%pi/3) + 2*%e^(1/5);
z = (x + y)/2;
disp('x =', x, 'y =', y, 'z =', z)

// 3. Представление результатов с разным числом знаков и в экспоненциальном формате
format('v', 5);
disp('Формат v, 5 знаков:', 'x =', x, 'y =', y, 'z =', z)
format('v', 8);
disp('Формат v, 8 знаков:', 'x =', x, 'y =', y, 'z =', z)
format('e', 8);
disp('Экспоненциальный формат, 8 знаков:', 'x =', x, 'y =', y, 'z =', z)
format('v', 10); // формат по умолчанию

// 4. Векторы и матрицы
v1 = [3; 7; -2; 10; 5];
v2 = [3 7 -2 10 5];
v3 = 2:3:26;
disp('v1 =', v1, 'v2 =', v2, 'v3 =', v3)

n = 5;
my_number = 27;
A = ceil(rand(n,n) * (10 + my_number));
B = ceil(rand(n,n) * (10 + my_number));
disp('A =', A, 'B =', B)

// 5. Операции над матрицами A и B
C = A + B;
disp('Сложение A + B:', C)

D = A * 5;
disp('Умножение A на скаляр 5:', D)

E1 = A .* B;
disp('Поэлементное умножение A.*B:', E1)
E2 = A * B;
disp('Матричное умножение A*B:', E2)

V2 = v2 * A;
disp('Умножение вектора v2 на матрицу A:', V2)
V1 = B * v1;
disp('Умножение матрицы B на вектор v1:', V1)

F1 = A / B;
disp('Деление A на B слева направо:', F1)
F2 = A \ B;
disp('Деление A на B справа налево:', F2)

G1 = B ^ 2;
disp('Возведение матрицы B во вторую степень:', G1)
G2 = B .^ 2;
disp('Возведение всех элементов B во вторую степень:', G2)

// 6. Характеристики матрицы A
A_T = A';
disp('Транспонированная A:', A_T)
A_inv = inv(A);
disp('Обратная матрица A:', A_inv)
A_det = det(A);
disp('Определитель A:', A_det)
A_diag = diag(A);
disp('Главная диагональ A:', A_diag)

sum_cols = sum(A, 'r');
sum_rows = sum(A, 'c');
sum_ttl = sum(A);
disp('Сумма по столбцам A:', sum_cols, 'сумма по строкам A:', sum_rows, 'сумма всех элементов A:', sum_ttl)

prod_cols = prod(A, 'r');
prod_rows = prod(A, 'c');
prod_ttl = prod(A);
disp('Произведение по столбцам A:', prod_cols, 'произведение по строкам A:', prod_rows, 'произведение всех элементов A:', prod_ttl)

[min_cols_val, min_cols_ind] = min(A, 'r');
[max_cols_val, max_cols_ind] = max(A, 'r');
[min_rows_val, min_rows_ind] = min(A, 'c');
[max_rows_val, max_rows_ind] = max(A, 'c');
disp('Минимум по столбцам A:', min_cols_val, 'индексы:', min_cols_ind)
disp('Максимум по столбцам A:', max_cols_val, 'индексы:', max_cols_ind)
disp('Минимум по строкам A:', min_rows_val, 'индексы:', min_rows_ind)
disp('Максимум по строкам A:', max_rows_val, 'индексы:', max_rows_ind)

min_ttl = min(A);
max_ttl = max(A);
disp('Минимальный элемент A:', min_ttl, 'максимальный элемент A:', max_ttl)

A_trace = trace(A);
A_size = size(A);
disp('След матрицы A:', A_trace, 'размер матрицы A:', A_size)

// 8. Матрица C и подматрицы (диапазон [-7, 9], n = 5)
n = 5;
C = rand(n,n) * (9 - (-7)) + (-7);
disp('C =', C)

C1 = C(3:5, 1:3);
disp('C1 (строки 3-5, столбцы 1-3):', C1)

C2 = C;
C2(3, :) = [];
disp('C2 (без 3-й строки):', C2)

C3 = C(:, [1 4 3 2 5]);
disp('C3 (столбцы 2 и 4 переставлены):', C3)

// 9-10. Решение СЛАУ Ax = b
A = [-3 7 1; -3 -9 -5; 0 0 -1];
b = [0; 2; 1];
disp('A =', A, 'b =', b)

// а) метод обратной матрицы
x_inv = A\b;
disp('Решение методом обратной матрицы:', x_inv)

// б) метод Крамера
D = det(A);
A1 = A; A1(:,1) = b;
A2 = A; A2(:,2) = b;
A3 = A; A3(:,3) = b;
d(1) = det(A1);
d(2) = det(A2);
d(3) = det(A3);
x_cramer = d/D;
disp('Решение методом Крамера:', x_cramer)

// в) метод Жордана-Гаусса
C = rref([A b]);
[n, m] = size(C);
x_gauss = C(:, m);
disp('Решение методом Жордана-Гаусса:', x_gauss)

// Проверка всех трёх решений
check1 = A * x_inv;
check2 = A * x_cramer;
check3 = A * x_gauss;
disp('Проверка (обратная матрица), A*x =', check1)
disp('Проверка (Крамер), A*x =', check2)
disp('Проверка (Жордан-Гаусс), A*x =', check3)
