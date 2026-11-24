"""Простой калькулятор с графическим интерфейсом."""
import math
import tkinter as tk
from tkinter import messagebox
import calculator as calc


def read_number(entry):
    try:
        number = float(entry.get().strip().replace(',', '.'))
    except ValueError:
        raise ValueError('Введите число в нужное поле')
    if not math.isfinite(number):
        raise ValueError('Введите обычное конечное число')
    return number


def show(value):
    result.set(f'Результат: {value}')
    return value


def run(operation, needs_second=True):
    try:
        first = read_number(first_entry)
        value = operation(first, read_number(second_entry)) if needs_second else operation(first)
        show(value)
    except (ValueError, OverflowError) as error:
        messagebox.showerror('Ошибка', str(error))


def save_memory():
    try:
        calc.memory_save(read_number(first_entry))
        memory_label.set(f'Память: {calc.memory_read()}')
    except ValueError as error:
        messagebox.showerror('Ошибка', str(error))


def add_to_memory():
    try:
        calc.memory_add(read_number(first_entry))
        memory_label.set(f'Память: {calc.memory_read()}')
    except ValueError as error:
        messagebox.showerror('Ошибка', str(error))


def read_memory():
    first_entry.delete(0, tk.END)
    first_entry.insert(0, str(calc.memory_read()))
    show(calc.memory_read())


def clear_memory():
    calc.memory_clear()
    memory_label.set('Память: 0')


window = tk.Tk()
window.title('Калькулятор')
window.geometry('390x340')
window.resizable(False, False)

tk.Label(window, text='Первое число:').grid(row=0, column=0, padx=8, pady=8, sticky='w')
first_entry = tk.Entry(window, width=18)
first_entry.grid(row=0, column=1, columnspan=2, sticky='w')
tk.Label(window, text='Второе число:').grid(row=1, column=0, padx=8, pady=8, sticky='w')
second_entry = tk.Entry(window, width=18)
second_entry.grid(row=1, column=1, columnspan=2, sticky='w')
tk.Label(window, text='Для корня, факториала и памяти нужно первое число.', wraplength=360).grid(row=2, column=0, columnspan=4, pady=4)

buttons = [
    ('+', lambda: run(calc.add)), ('−', lambda: run(calc.subtract)),
    ('×', lambda: run(calc.multiply)), ('÷', lambda: run(calc.divide)),
    ('Степень', lambda: run(calc.power)), ('Корень', lambda: run(calc.square_root, False)),
    ('Факториал', lambda: run(calc.factorial, False)),
    ('MS', save_memory), ('MR', read_memory), ('M+', add_to_memory), ('MC', clear_memory),
]
for index, (name, action) in enumerate(buttons):
    tk.Button(window, text=name, width=9, command=action).grid(
        row=3 + index // 4, column=index % 4, padx=3, pady=4
    )

result = tk.StringVar(value='Результат: —')
memory_label = tk.StringVar(value='Память: 0')
tk.Label(window, textvariable=result, wraplength=360).grid(row=6, column=0, columnspan=4, pady=8)
tk.Label(window, textvariable=memory_label).grid(row=7, column=0, columnspan=4)
tk.Label(window, text='MS — сохранить, MR — прочитать, M+ — добавить, MC — очистить',
         wraplength=370).grid(row=8, column=0, columnspan=4, pady=8)
window.mainloop()
