"""Вычисления и память калькулятора."""
import math

memory = 0.0


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError('На ноль делить нельзя')
    return a / b


def power(a, b):
    if a == 0 and b < 0:
        raise ValueError('Ноль нельзя возвести в отрицательную степень')
    result = a ** b
    if isinstance(result, complex):
        raise ValueError('Результат не является действительным числом')
    return result


def square_root(a):
    if a < 0:
        raise ValueError('Нельзя извлечь корень из отрицательного числа')
    return math.sqrt(a)


def factorial(a):
    if not math.isfinite(a) or a < 0 or int(a) != a:
        raise ValueError('Факториал считается для целых неотрицательных чисел')
    if a > 170:
        raise ValueError('Для факториала введите число от 0 до 170')
    return math.factorial(int(a))


def memory_save(value):
    global memory
    memory = value


def memory_read():
    return memory


def memory_add(value):
    global memory
    memory += value


def memory_clear():
    global memory
    memory = 0.0
