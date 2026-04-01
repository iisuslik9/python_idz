import tkinter as tk
from tkinter import messagebox
from model import ArmatureWarehouseModel

class ArmatureWarehouseController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
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
        
        self.view.set_output(result)

    def handle_save(self):
        filename = self.view.save_file_dialog()
        if filename:
            try:
                content = self.view.output_text.get("1.0", tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("ПРОЕКТИРОВАНИЕ СКЛАДА АРМАТУРЫ\n")
                    f.write("=" * 40 + "\n\n")
                    f.write(content)
                messagebox.showinfo("Успех", f"Результат сохранен в {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")