import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

class ArmatureWarehouseView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Проектирование склада арматуры (Вариант 4)")
        self.root.geometry("600x700")
        self.root.minsize(500, 600)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self._build_ui()

    def _build_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)

        # 1. Годовая потребность
        input_frame1 = ttk.LabelFrame(main_frame, text="Годовая потребность в арматуре Пга, т", padding="10")
        input_frame1.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame1.columnconfigure(1, weight=1)

        ttk.Label(input_frame1, text="Значение:").grid(row=0, column=0, sticky=tk.W)
        self.entry_pga = ttk.Entry(input_frame1, font=("Arial", 11))
        self.entry_pga.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        ttk.Label(input_frame1, text="т", font=("Arial", 9)).grid(row=0, column=2, padx=(5, 0))

        self.msg_pga = ttk.Label(input_frame1, text="", foreground="red", font=("Arial", 9))
        self.msg_pga.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(2, 0))

        # 2. Запас арматуры (ползунок 20-25 сут)
        input_frame2 = ttk.LabelFrame(main_frame, text="Запас арматурной стали na, сут (20-25)", padding="10")
        input_frame2.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame2.columnconfigure(1, weight=1)

        self.na_var = tk.IntVar(value=22)
        
        scale = tk.Scale(input_frame2, 
                        from_=20, 
                        to=25, 
                        variable=self.na_var, 
                        orient=tk.HORIZONTAL, 
                        length=300,
                        resolution=1,  
                        font=("Arial", 10))
        scale.grid(row=0, column=0, sticky=tk.W, pady=5)

        # 3. Годовой фонд времени
        input_frame3 = ttk.LabelFrame(main_frame, text="Годовой фонд рабочего времени Ba, сут", padding="10")
        input_frame3.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame3.columnconfigure(1, weight=1)

        ttk.Label(input_frame3, text="Значение:").grid(row=0, column=0, sticky=tk.W)
        self.entry_ba = ttk.Entry(input_frame3, font=("Arial", 11))
        self.entry_ba.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        ttk.Label(input_frame3, text="сут", font=("Arial", 9)).grid(row=0, column=2, padx=(5, 0))

        self.msg_ba = ttk.Label(input_frame3, text="", foreground="red", font=("Arial", 9))
        self.msg_ba.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(2, 0))

        # 4. Вместимость склада (Combobox)
        capacity_frame = ttk.LabelFrame(main_frame, text="Вместимость склада", padding="10")
        capacity_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        capacity_frame.columnconfigure(1, weight=1)

        ttk.Label(capacity_frame, text="Тип:").grid(row=0, column=0, sticky=tk.W)
        self.capacity_var = tk.StringVar(value="до 500т")
        capacity_combo = ttk.Combobox(capacity_frame, textvariable=self.capacity_var, 
                                    values=["до 500т", "свыше 500т"], state="readonly", width=15)
        capacity_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))

        # 5. Тип металла (Combobox)
        metal_frame = ttk.LabelFrame(main_frame, text="Тип арматуры qa, т/м²", padding="10")
        metal_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        metal_frame.columnconfigure(1, weight=1)

        ttk.Label(metal_frame, text="Тип:").grid(row=0, column=0, sticky=tk.W)
        self.metal_var = tk.StringVar(value="сталь в прутках")
        metal_combo = ttk.Combobox(metal_frame, textvariable=self.metal_var,
                                 values=["сталь в бухтах", "сталь в прутках", "полосовая сталь", 
                                        "сетки в рулонах", "бухты в бункерах"], 
                                 state="readonly", width=20)
        metal_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))

        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, pady=20)
        
        self.calc_button = ttk.Button(button_frame, text="Рассчитать")
        self.calc_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_button = ttk.Button(button_frame, text="Сохранить в файл", state="disabled")
        self.save_button.pack(side=tk.LEFT)

        # Результат
        output_frame = ttk.LabelFrame(main_frame, text="Результат расчета", padding="10")
        output_frame.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.output_text = tk.Text(output_frame, height=8, wrap=tk.WORD, font=("Consolas", 10))
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.output_text.configure(yscrollcommand=scrollbar.set)

    # API для Controller
    def clear_messages(self):
        """Очищает все красные сообщения"""
        self.msg_pga.config(text="")
        self.msg_ba.config(text="")

    def set_message(self, field, message):
        """Устанавливает красное сообщение для поля"""
        if field == "pga":
            self.msg_pga.config(text=message)
        elif field == "ba":
            self.msg_ba.config(text=message)

    def get_input(self):
        return {
            "annual_demand": self.entry_pga.get(),
            "storage_days": self.na_var.get(),
            "work_days": self.entry_ba.get(),
            "capacity_type": self.capacity_var.get(),
            "metal_type": self.metal_var.get()
        }

    def set_output(self, result):
        self.clear_messages()
        self.output_text.delete("1.0", tk.END)
        if isinstance(result, dict):
            self.output_text.insert(tk.END, f"Площадь склада S = {result['area']} м²\n\n")
            self.output_text.insert(tk.END, result['details'])
            self.save_button.config(state="normal")
        else:
            self.output_text.insert(tk.END, result)
            self.save_button.config(state="disabled")

    def set_handlers(self, calc_handler, save_handler):
        self.calc_button.config(command=calc_handler)
        self.save_button.config(command=save_handler)

    def save_file_dialog(self):
        return filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Сохранить результат в Excel"
        )

    def start(self):
        self.root.mainloop()