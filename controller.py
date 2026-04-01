import tkinter as tk
from tkinter import messagebox
from model import ArmatureWarehouseModel
import pandas as pd

class ArmatureWarehouseController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_result = None
        self.view.set_handlers(self.handle_calculate, self.handle_save)

    def handle_calculate(self):
        self.view.clear_messages() 
        data = self.view.get_input()
        
        result = self.model.calculate_area(**data)
        
    
        if isinstance(result, str):
            # Определяем к какому полю относится ошибка
            if "годовая потребность" in result:
                self.view.set_message("pga", result)
            elif "запас" in result:
                self.view.set_message("pga", result)  
            elif "фонд времени" in result:
                self.view.set_message("ba", result)
            self.current_result = None
            self.view.clear_output()
        else:
            self.current_result = result
            self.view.set_output(result)

    def handle_save(self):
        if self.current_result is None:
            messagebox.showwarning("Предупреждение", "Сначала выполните расчет")
            return
        filename = self.view.save_file_dialog()
        if filename:
            try:
                self.save_to_excel(filename, self.current_result)
                messagebox.showinfo("Успех", f"Результат сохранен в {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")


    def save_to_excel(self, filename, result):
        data = {
            "Параметр": ["Площадь склада"],
            "Значение": [f"{result['area']} м\u00B2"]
        }
        
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)