import tkinter as tk
from tkinter import messagebox
from model import WarehouseModel
from view import WarehouseView

class WarehouseController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.controller = self  # Передаем ссылку на контроллер

    def calculate(self):
        try:
            self.model.set_data('Pa', float(self.view.Pa_entry.get()))
            self.model.set_data('V', float(self.view.V_entry.get()))
            self.model.set_data('capacity', float(self.view.capacity_entry.get()))
            self.model.set_data('type', self.view.type_combo.get())
            self.model.set_data('p', self.view.p_var.get())
            S = self.model.calculate_area()
            self.view.show_result(S)
        except ValueError as e:
            self.view.show_error('Введите корректные числа!')
        except KeyError as e:
            self.view.show_error('Выберите тип арматуры!')

    def save(self, filename: str):
        try:
            S = self.model.calculate_area()
            self.model.save_to_xlsx(filename, S)
            messagebox.showinfo('Успех', f'Сохранено в {filename}')
        except Exception as e:
            messagebox.showerror('Ошибка', 'Не удалось сохранить файл')