import math
import cmath

def task1(x, y):
    if x > 0 and y < 0:
        return x + y
    elif x > 0 and y > 1:
        return 1
    else:
        return x - y

def task2(a):
    if a <= 0:
        return None
    arg1 = (a**2 + math.sqrt(a)) / (1 + (math.sin(a)**2) / (2*a))
    arg2 = 2.5 / (2 * math.log(a))
    return math.sqrt(math.cos(arg1) + arg2)

def task3(a, b):
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

def task4(n):
    divisors = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return sorted(divisors)

def task5(a, b):
    total = 0
    for i in range(max(a, 4), b + 1, 4):
        total += i
    return total

def task6(n):
    return len(str(n))

def task7(x):
    epsilon = 1e-5
    s = 0
    term = 1
    k = 1
    fact = 1
    while abs(term) >= epsilon:
        term = ((-1)**(k//2) * (x**k)) / fact
        s += term
        k += 2
        fact *= k * (k - 1)
    return s

def task8(x):
    epsilon = 1e-4
    if abs(x) >= 0.5:
        return None
    s = 0
    term = 1
    n = 0
    x_pow = 1
    while abs(term) >= epsilon:
        coeff = (1 + ((-1)**n * 2**(n + 1)))
        term = coeff * x_pow
        s += term
        n += 1
        x_pow *= x
    return s

def task9():
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
            print("Возникла ошибка: Вы ввели не число!")

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Возникла ошибка: Вы ввели не число!")

def get_positive_float(prompt):
    while True:
        try:
            val = float(input(prompt))
            if val <= 0:
                print("Ошибка: Введите положительное число!")
            else:
                return val
        except ValueError:
            print("Возникла ошибка: Вы ввели не число!")

def main():
    while True:
        print("\n" + "="*50)
        print("ВЫБЕРИТЕ ЗАДАНИЕ (1-9) или 0 для выхода:")
        print("="*50)
        print("1. f(x,y)")
        print("2. F(a)")
        print("3. Обработка двух чисел")
        print("4. Делители числа")
        print("5. Сумма кратных 4")
        print("6. Количество цифр")
        print("7. Ряд sin(x)")
        print("8. Геометрический ряд")
        print("9. 100 простых чисел")
        print("0. ВЫХОД")
        print("-"*50)
        
        choice = input("Ваш выбор: ").strip()
        
        if choice == '0':
            print("До свидания!")
            break
            
        if choice not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            print("Ошибка: Введите число от 0 до 9!")
            continue
            
        choice = int(choice)
        
        try:
            if choice == 1:
                print("\nЗадание 1: f(x,y)")
                x = get_float("Введите x: ")
                y = get_float("Введите y: ")
                result = task1(x, y)
                print(f"f({x}, {y}) = {result}")
                
            elif choice == 2:
                print("\nЗадание 2: F(a)")
                a = get_positive_float("Введите a (>0): ")
                result = task2(a)
                if result is None:
                    print("Ошибка: a должно быть > 0!")
                else:
                    print(f"F({a}) = {result:.6f}")
                    
            elif choice == 3:
                print("\nЗадание 3: Обработка двух чисел")
                a = get_float("Введите первое число a: ")
                b = get_float("Введите второе число b: ")
                result_a, result_b = task3(a, b)
                print(f"a' = {result_a}, b' = {result_b}")
                
            elif choice == 4:
                print("\nЗадание 4: Делители числа")
                n = get_int("Введите натуральное число N: ")
                if n <= 0:
                    print("Ошибка: N должно быть натуральным!")
                else:
                    divisors = task4(n)
                    print(f"Делители {n}: {', '.join(map(str, divisors))}")
                    
            elif choice == 5:
                print("\nЗадание 5: Сумма кратных 4")
                a = get_int("Введите A: ")
                b = get_int("Введите B: ")
                if a > b:
                    print("Предупреждение: A > B, поменяем местами")
                    a, b = b, a
                result = task5(a, b)
                print(f"Сумма чисел кратных 4 в [{a}, {b}] = {result}")
                
            elif choice == 6:
                print("\nЗадание 6: Количество цифр")
                n = get_int("Введите натуральное число N: ")
                if n <= 0:
                    print("Ошибка: N должно быть натуральным!")
                else:
                    result = task6(n)
                    print(f"Количество цифр в {n}: {result}")
                    
            elif choice == 7:
                print("\nЗадание 7: Ряд sin(x)")
                x = get_float("Введите x (-π ≤ x ≤ π): ")
                if abs(x) > math.pi:
                    print("Предупреждение: |x| > π, результат может быть неточным")
                result = task7(x)
                check = math.sin(x)
                print(f"S ≈ {result:.6f}")
                print(f"sin({x}) = {check:.6f}")
                print(f"Погрешность: {abs(result - check):.2e}")
                
            elif choice == 8:
                print("\nЗадание 8: Геометрический ряд")
                x = get_float("Введите x (|x| < 0.5): ")
                if abs(x) >= 0.5:
                    print("Ошибка: |x| должно быть < 0.5!")
                else:
                    result = task8(x)
                    denom = (1 - x) * (1 + 2 * x)
                    check = 3 / denom if denom != 0 else float('inf')
                    print(f"S ≈ {result:.6f}")
                    print(f"f({x}) = {check:.6f}")
                    
            elif choice == 9:
                print("\nЗадание 9: 100 простых чисел")
                primes = task9()
                print("Первые 100 простых чисел:")
                print(", ".join(map(str, primes[:10])))
                print("...")
                print(", ".join(map(str, primes[-10:])))
                print(f"Всего найдено: {len(primes)}")
                
        except Exception as e:
            print(f"Возникла ошибка: {str(e)}")

if __name__ == "__main__":
    main()
