import math
import cmath

def piecewise_function(x, y):
    if x > 0 and y < 0:
        return x + y
    elif x > 0 and y > 1:
        return 1
    else:
        return x - y

def complex_function(a):
    #a = 1e-15
    if a <= 0:
        return None
    arg1 = (a**2 + cmath.sqrt(a)) / (1 + (cmath.sin(a)**2) / (2*a))
    arg2 = 2.5 / (2 * cmath.log(a))
    return cmath.sqrt(cmath.cos(arg1) + arg2)

def process_two_numbers(a, b):
    if a == 0 or b == 0:
        return a, b
    if a > 0 and b > 0:
        if a > b:
            return -a, b
        else:
            return a, -b
    elif a < 0 and b < 0:
        return a * 2, b * 3
    else:
        if abs(a) < abs(b):
            return (a + b) / 2, b - 1
        else:
            return (a + b) / 2, a - 1

def find_divisors(n):
    divisors = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return sorted(divisors)

def sum_multiples_of_four(a, b):
    total = 0
    # Находим первое число >= a, которое делится на 4
    start = a + (4 - a % 4) % 4
    for i in range(start, b + 1, 4):
        total += i
    return total

def count_digits(n):
    return len(str(n))

def taylor_sin_series(x):
    #ряд sin(x) с точностью 10^-5
    
    if x == 0:
        return 1.0
    epsilon = 1e-5
    sum = 0
    term = 1
    n = 1
    while abs(term) >= epsilon:
        sum += term
        term *= (-x**2) / ((2 * n) * (2 * n + 1))
        n += 1
    return sum

def geometric_series_sum(x):
    epsilon = 1e-4
    if abs(x) >= 0.5:
        return None
    s = 0
    
    x_pow = 1.0 # хранит x^n
    minus_2x_pow = 1.0  # хранит (-2x)^n
    n = 0
    while True:
        term = x_pow + 2 * minus_2x_pow
        
        if abs(term) < epsilon:
            break
            
        s += term

        x_pow *= x
        minus_2x_pow *= (-2 * x)
        n += 1
        if n > 10000: break #если ряд расходится
    return s

def first_hundred_primes():
    primes = []
    num = 2
    while len(primes) < 100:
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 1
    return primes

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("введите число")

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("введите целое число!")

def get_positive_float(prompt):
    while True:
        val = get_float(prompt)
        if val > 0:
            return val
        print("введите положительное число!")

def show_menu():
    print("выберите задания (1-9) или 0 для выхода:")
    print("-"*50)

def handle_piecewise_function():
    x = get_float("введите x: ")
    y = get_float("введите y: ")
    result = piecewise_function(x, y)
    print(f"f({x}, {y}) = {result}")

def handle_complex_function():
    a = get_positive_float("Введите a > 0: ")
    result = complex_function(a)

    c_result = complex(result) 
    imag_part = abs(c_result.imag) 
    print(f"Результат: {c_result.real:10.6f} + {c_result.imag:10.6f}i")
    print(f"|imag| = {imag_part:.2e}")
    
    if  imag_part > 1e-12:  # только если есть мнимая часть
        print(f"F({a}) = {c_result:+.6f}")  # автоматический знак
    else:
        print(f"F({a}) = {c_result.real:.6f}")

def handle_number_processing():
    a = get_float("введите число a: ")
    b = get_float("введите число b: ")
    result_a, result_b = process_two_numbers(a, b)
    print(f"a' = {result_a}, b' = {result_b}")

def handle_divisors():
    n = get_int("введите натуральное число N: ")
    if n <= 0:
        print("N должно быть натуральным")
        return
    divisors = find_divisors(n)
    print(f"делители {n}: {', '.join(map(str, divisors))}")

def handle_sum_multiples():
    a = get_int("введите A: ")
    b = get_int("введите B: ")
    if a > b:
        print("смена границ")
        a, b = b, a
    result = sum_multiples_of_four(a, b)
    print(f"сумма чисел кратных 4 в [{a}, {b}] = {result}")

def handle_digit_count():
    n = get_int("введите натуральное число N: ")
    if n <= 0:
        print("N должно быть натуральным!")
        return
    result = count_digits(n)
    print(f"rоличество цифр в {n}: {result}")

def handle_sin_series():
    x = get_float("Введите x (-pi ≤ x ≤ pi): ")
    #x = math.pi / 2
    if abs(x) > math.pi:
        print("x выходит за пределы [-pi, pi]")
    result = taylor_sin_series(x)
    check = math.sin(x) / x if x != 0 else 1.0
    print(f"S ≈ {result:.6f}")
    print(f"f(x) = {check:.6f}")
    print(f"Погрешность: {abs(result - check):.2e}")

def handle_geometric_series():
    x = get_float("Введите x (|x| < 0.5): ")
    if abs(x) >= 0.5:
        print("|x| должно быть < 0.5")
        return
    result = geometric_series_sum(x)
    denom = (1 - x) * (1 + 2 * x)
    check = 3 / denom
    print(f"S ≈ {result:.6f}")
    print(f"f({x}) = {check:.6f}")

def handle_prime_numbers():
    primes = first_hundred_primes()
    print("первые 100 простых чисел:")
    print(", ".join(map(str, primes)))


def dispatch_choice(choice_str):
    choice_str = choice_str.strip()
    
    match choice_str:
        case '0':
            print("программа завершилась")
            return True  
        case '1':
            handle_piecewise_function()
        case '2':
            handle_complex_function()
        case '3':
            handle_number_processing()
        case '4':
            handle_divisors()
        case '5':
            handle_sum_multiples()
        case '6':
            handle_digit_count()
        case '7':
            handle_sin_series()
        case '8':
            handle_geometric_series()
        case '9':
            handle_prime_numbers()
        case _:
            print("введите число от 0 до 9!")
            return False
    return False

def main():
    while True:
        show_menu()
        if dispatch_choice(input("выбрана задача: ")):
            break

if __name__ == "__main__":
    main()
