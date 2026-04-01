import tkinter as tk
from tkinter import ttk
from typing import Callable

class WarehouseView(ttk.Frame):
    def __init__(self, parent, controller: Callable):
        super().__init__(parent)
        self.controller = controller
        self.result_var = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        # Па, т
        ttk.Label(self, text='Па (т):').grid(row=0, column=0)
        self.Pa_entry = ttk.Entry(self)
        self.Pa_entry.grid(row=0, column=1)

        # В, сут
        ttk.Label(self, text='В (сут):').grid(row=1, column=0)
        self.V_entry = ttk.Entry(self)
        self.V_entry.grid(row=1, column=1)

        # Вместимость, т (для Ka)
        ttk.Label(self, text='Вместимость (т):').grid(row=2, column=0)
        self.capacity_entry = ttk.Entry(self)
        self.capacity_entry.grid(row=2, column=1)

        # Тип арматуры (Combobox)
        ttk.Label(self, text='Тип qa (т/м²):').grid(row=3, column=0)
        self.type_combo = ttk.Combobox(self, values=['бухты/мотки', 'прутки', 'полосовая', 'сетки', 'бухты в бункерах'])
        self.type_combo.grid(row=3, column=1)

        # Запас п (Scale 20-25 сут)
        ttk.Label(self, text='Запас п (сут):').grid(row=4, column=0, sticky='w')
        self.p_var = tk.IntVar(value=22)  # Целое число
        self.p_scale = tk.Scale(
            self, 
            from_=20, 
            to=25, 
            variable=self.p_var, 
            orient='horizontal',
            length=200,
            resolution=1.0
        )
        self.p_scale.grid(row=4, column=1, sticky='ew')

        ttk.Label(self, textvariable=self.p_var).grid(row=4, column=2)

        ttk.Button(self, text='Рассчитать', command=self.calculate).grid(row=5, column=0)
        ttk.Button(self, text='Сохранить в XLSX', command=self.save).grid(row=5, column=1)

    
        # Отображение текущего значения
        self.p_label = ttk.Label(self, textvariable=self.p_var)
        self.p_label.grid(row=4, column=2, sticky='w')
        ttk.Label(self, text='сут').grid(row=4, column=3)

        # Результат
        ttk.Label(self, text='Площадь S (м²):').grid(row=6, column=0)
        ttk.Label(self, textvariable=self.result_var).grid(row=6, column=1)

    def calculate(self):
        self.controller.calculate()

    def save(self):
        self.controller.save('warehouse.xlsx')

    def show_result(self, S: float):
        self.result_var.set(str(S))

    def show_error(self, msg: str):
        tk.messagebox.showerror('Ошибка', msg)