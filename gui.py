import os
import sys
from datetime import datetime
from typing import Optional
import tkinter as tk
from tkinter import messagebox, ttk

# Настройка путей, чтобы Python видел пакеты
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import DATABASE_DSN, DATABASE_URL
from database.sql_repository import SQLRepository
from database.orm_repository import ORMRepository
from service.logistics_service import LogisticsService
from service.exceptions import (
    DuplicateEntityError,
    EntityNotFoundError,
    InvalidStatusError,
    VALID_STATUSES,
    WarehouseCapacityExceededError,
)


class LogisticsGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Логистика — графический интерфейс")
        self.geometry("980x640")
        self.minsize(900, 560)

        self.service: Optional[LogisticsService] = None
        self.action_buttons: list[ttk.Button] = []
        self.form_widgets: dict[str, tuple[tk.Widget, dict]] = {}
        self.form_action = None

        self._build_ui()

    def _build_ui(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(top_frame, text="Выберите режим работы с базой данных:").pack(side=tk.LEFT, padx=(0, 8))

        self.db_mode = tk.StringVar(value="sql")
        ttk.Radiobutton(top_frame, text="SQL (psycopg2)", variable=self.db_mode, value="sql").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(top_frame, text="ORM (SQLAlchemy)", variable=self.db_mode, value="orm").pack(side=tk.LEFT, padx=5)

        ttk.Button(top_frame, text="Подключиться", command=self.connect_database).pack(side=tk.LEFT, padx=16)

        self.status_label = ttk.Label(top_frame, text="Статус: не подключено")
        self.status_label.pack(side=tk.LEFT, padx=8)

        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        controls_frame = ttk.LabelFrame(content_frame, text="Операции")
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=5)

        actions = [
            ("Добавить склад", self.add_warehouse),
            ("Добавить груз", self.add_shipment),
            ("Добавить водителя", self.add_driver),
            ("Назначить водителя", self.assign_driver_to_shipment),
            ("Грузы на складе", self.show_shipments_by_warehouse),
            ("Обновить груз", self.update_shipment),
            ("Рейтинг водителей", self.driver_rankings),
            ("Удалить груз", self.delete_shipment),
            ("Удалить склад", self.delete_warehouse),
            ("Инфо по складам", self.show_warehouses_info),
            ("Очистить лог", self.clear_log),
            ("Выход", self.quit),
        ]

        for label, command in actions:
            button = ttk.Button(controls_frame, text=label, command=command, state=tk.DISABLED)
            button.pack(fill=tk.X, pady=3, padx=4)
            self.action_buttons.append(button)

        self.form_frame = ttk.LabelFrame(content_frame, text="Форма записи")
        self.form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)

        self.form_title = ttk.Label(self.form_frame, text="Выберите операцию", font=(None, 11, "bold"))
        self.form_title.pack(anchor=tk.W, padx=10, pady=(10, 4))

        self.form_fields_frame = ttk.Frame(self.form_frame)
        self.form_fields_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        self.form_submit_button = ttk.Button(self.form_frame, text="Выполнить", command=self.submit_form, state=tk.DISABLED)
        self.form_submit_button.pack(side=tk.BOTTOM, pady=10)

        log_frame = ttk.LabelFrame(self, text="Журнал операций")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.log_text = tk.Text(log_frame, state=tk.DISABLED, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=(4, 0), pady=4)

        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 4), pady=4)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log("Программа запущена. Подключитесь к базе данных, чтобы начать работу.")

    def connect_database(self):
        mode = self.db_mode.get()
        try:
            if mode == "sql":
                repository = SQLRepository(DATABASE_DSN)
                mode_name = "SQL"
            else:
                repository = ORMRepository(DATABASE_URL)
                mode_name = "ORM"

            self.service = LogisticsService(repository=repository)
            self.status_label.config(text=f"Статус: подключено ({mode_name})")
            self.set_buttons_state(True)
            self.log(f"Подключено к базе данных: {mode_name}")
            messagebox.showinfo("Успех", f"Подключение к базе данных выполнено: {mode_name}")
        except Exception as exc:
            self.show_error("Ошибка подключения", exc)

    def set_buttons_state(self, enabled: bool):
        state = tk.NORMAL if enabled else tk.DISABLED
        for button in self.action_buttons:
            button.config(state=state)

    def log(self, message: str):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{datetime.now():%Y-%m-%d %H:%M:%S} — {message}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def show_error(self, title: str, exc: Exception):
        message = str(exc)
        messagebox.showerror(title, message)
        self.log(f"Ошибка: {message}")

    def clear_log(self):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def clear_form(self):
        for child in self.form_fields_frame.winfo_children():
            child.destroy()
        self.form_widgets.clear()
        self.form_action = None
        self.form_title.config(text="Выберите операцию")
        self.form_submit_button.config(text="Выполнить", state=tk.DISABLED)

    def create_form(self, title: str, fields: list[dict], action):
        self.clear_form()
        self.form_title.config(text=title)
        self.form_action = action

        for field in fields:
            label = ttk.Label(self.form_fields_frame, text=field["label"])
            label.pack(anchor=tk.W, pady=(8, 2), padx=2)

            if field.get("type") == "combobox":
                entry = ttk.Combobox(self.form_fields_frame, values=field.get("values", []), state="readonly")
                entry.set(field.get("default", ""))
            else:
                entry = ttk.Entry(self.form_fields_frame)
                default = field.get("default")
                if default is not None:
                    entry.insert(0, str(default))

            entry.pack(fill=tk.X, padx=2)
            self.form_widgets[field["name"]] = (entry, field)

        self.form_submit_button.config(text="Сохранить", state=tk.NORMAL)

    def submit_form(self):
        if self.service is None or not self.form_action:
            return

        try:
            cleaned = {}
            for name, (widget, meta) in self.form_widgets.items():
                raw = widget.get().strip()
                if raw == "" and meta.get("required", False):
                    raise ValueError(f"Поле '{meta['label']}' обязательно для заполнения")

                if raw == "" and not meta.get("required", False):
                    cleaned[name] = None
                    continue

                value_type = meta.get("value_type", str)
                if value_type == int:
                    cleaned[name] = int(raw)
                elif value_type == float:
                    cleaned[name] = float(raw)
                else:
                    cleaned[name] = raw

            self.form_action(**cleaned)
        except Exception as exc:
            self.show_error("Ошибка формы", exc)

    def add_warehouse(self):
        if self.service is None:
            return

        fields = [
            {"name": "name", "label": "Название склада:", "required": True, "value_type": str},
            {"name": "location", "label": "Адрес склада:", "required": True, "value_type": str},
            {"name": "capacity", "label": "Вместимость склада (тонн):", "required": True, "value_type": float},
        ]
        self.create_form("Добавить склад", fields, self.submit_add_warehouse)

    def submit_add_warehouse(self, name: str, location: str, capacity: float):
        warehouse_id = self.service.register_new_warehouse(name.strip(), location.strip(), capacity)
        self.log(f"Склад добавлен: ID={warehouse_id}, '{name}', адрес '{location}', вместимость {capacity} тонн")
        messagebox.showinfo("Успех", f"Склад добавлен. ID: {warehouse_id}")
        self.clear_form()

    def _get_warehouse_choices(self):
        warehouses = self.service.repository.get_all_warehouses()
        choices = []
        self._warehouse_map = {}
        for wh in warehouses:
            display = f"{wh['name']} (ID {wh['id']})"
            choices.append(display)
            self._warehouse_map[display] = wh['id']
        return choices

    def add_shipment(self):
        if self.service is None:
            return

        warehouse_choices = self._get_warehouse_choices()
        if not warehouse_choices:
            messagebox.showwarning("Нет складов", "Сначала добавьте склад, затем заполните груз.")
            return

        fields = [
            {"name": "tracking", "label": "Трек-номер груза:", "required": True, "value_type": str},
            {"name": "weight", "label": "Вес груза (кг):", "required": True, "value_type": float},
            {
                "name": "status",
                "label": "Статус груза:",
                "required": True,
                "type": "combobox",
                "values": VALID_STATUSES,
                "default": VALID_STATUSES[0],
                "value_type": str,
            },
            {
                "name": "warehouse_label",
                "label": "Склад:",
                "required": True,
                "type": "combobox",
                "values": warehouse_choices,
                "default": warehouse_choices[0],
                "value_type": str,
            },
        ]
        self.create_form("Добавить груз", fields, self.submit_add_shipment)

    def submit_add_shipment(self, tracking: str, weight: float, status: str, warehouse_label: str):
        warehouse_id = self._warehouse_map.get(warehouse_label)
        if warehouse_id is None:
            raise ValueError("Выберите склад из списка")

        shipment_id = self.service.register_new_shipment(tracking.strip(), weight, status, warehouse_id)
        self.log(f"Груз добавлен: ID={shipment_id}, трек='{tracking}', вес={weight} кг, статус='{status}', склад={warehouse_label}")
        messagebox.showinfo("Успех", f"Груз добавлен. ID: {shipment_id}")
        self.clear_form()

    def add_driver(self):
        if self.service is None:
            return

        fields = [
            {"name": "name", "label": "ФИО водителя:", "required": True, "value_type": str},
            {"name": "license_number", "label": "Номер лицензии:", "required": True, "value_type": str},
        ]
        self.create_form("Добавить водителя", fields, self.submit_add_driver)

    def submit_add_driver(self, name: str, license_number: str):
        driver_id = self.service.register_new_driver(name.strip(), license_number.strip())
        self.log(f"Водитель добавлен: ID={driver_id}, '{name}', лицензия '{license_number}'")
        messagebox.showinfo("Успех", f"Водитель добавлен. ID: {driver_id}")
        self.clear_form()

    def assign_driver_to_shipment(self):
        if self.service is None:
            return

        fields = [
            {"name": "shipment_id", "label": "ID груза:", "required": True, "value_type": int},
            {"name": "driver_id", "label": "ID водителя:", "required": True, "value_type": int},
            {"name": "delivery_date", "label": "Дата доставки (ГГГГ-ММ-ДД):", "required": False, "value_type": str},
        ]
        self.create_form("Назначить водителя", fields, self.submit_assign_driver_to_shipment)

    def submit_assign_driver_to_shipment(self, shipment_id: int, driver_id: int, delivery_date: str | None):
        if delivery_date:
            delivery_date = datetime.strptime(delivery_date.strip(), "%Y-%m-%d").date()
        else:
            delivery_date = datetime.now().date()

        assignment_id = self.service.assign_driver_to_shipment(shipment_id, driver_id, delivery_date)
        self.log(f"Водитель назначен: shipment_id={shipment_id}, driver_id={driver_id}, дата={delivery_date}")
        messagebox.showinfo("Успех", f"Назначение выполнено. ID записи: {assignment_id}")
        self.clear_form()

    def show_shipments_by_warehouse(self):
        if self.service is None:
            return

        fields = [
            {"name": "warehouse_id", "label": "ID склада:", "required": True, "value_type": int},
        ]
        self.create_form("Грузы на складе", fields, self.submit_show_shipments_by_warehouse)

    def submit_show_shipments_by_warehouse(self, warehouse_id: int):
        shipments = self.service.get_warehouse_inventory(warehouse_id)
        if not shipments:
            self.log(f"Склад {warehouse_id}: грузов не найдено.")
            messagebox.showinfo("Грузы на складе", f"На складе {warehouse_id} грузы отсутствуют.")
            self.clear_form()
            return

        text = "".join(
            [
                f"ID={s['id']} | трек={s['tracking_number']} | вес={s['weight']} кг | статус={s['status']}\n"
                for s in shipments
            ]
        )
        self.log(f"Запрошены грузы для склада {warehouse_id}. Найдено {len(shipments)} позиций.")
        messagebox.showinfo("Грузы на складе", text)
        self.clear_form()

    def update_shipment(self):
        if self.service is None:
            return

        fields = [
            {"name": "shipment_id", "label": "ID груза:", "required": True, "value_type": int},
            {
                "name": "status",
                "label": "Новый статус (оставьте пустым, если не менять):",
                "required": False,
                "type": "combobox",
                "values": ["", *VALID_STATUSES],
                "default": "",
                "value_type": str,
            },
            {"name": "warehouse_id", "label": "Новый ID склада (оставьте пустым, если не менять):", "required": False, "value_type": int},
        ]
        self.create_form("Обновить груз", fields, self.submit_update_shipment)

    def submit_update_shipment(self, shipment_id: int, status: str | None, warehouse_id: int | None):
        if status is not None:
            status = status.strip() or None
        self.service.modify_shipment(shipment_id, status=status, warehouse_id=warehouse_id)
        self.log(f"Груз {shipment_id} обновлен. Статус={status}, склад={warehouse_id}")
        messagebox.showinfo("Успех", "Данные о грузе успешно обновлены.")
        self.clear_form()

    def driver_rankings(self):
        if self.service is None:
            return
        try:
            rankings = self.service.get_driver_rankings()
            if not rankings:
                self.log("Запрошен рейтинг водителей: водителей нет.")
                messagebox.showinfo("Рейтинг водителей", "Нет зарегистрированных водителей.")
                return

            text = "".join(
                [
                    f"ID={item['id']} | {item['name']} | лицензия={item['license_number']} | доставок={item['delivery_count']}\n"
                    for item in rankings
                ]
            )
            self.log(f"Запрошен рейтинг водителей. Найдено {len(rankings)} водителей.")
            messagebox.showinfo("Рейтинг водителей", text)
        except Exception as exc:
            self.show_error("Ошибка рейтинга водителей", exc)

    def delete_shipment(self):
        if self.service is None:
            return

        fields = [
            {"name": "shipment_id", "label": "ID груза:", "required": True, "value_type": int},
        ]
        self.create_form("Удалить груз", fields, self.submit_delete_shipment)

    def submit_delete_shipment(self, shipment_id: int):
        self.service.remove_shipment(shipment_id)
        self.log(f"Груз {shipment_id} удалён.")
        messagebox.showinfo("Успех", "Груз успешно удалён.")
        self.clear_form()

    def delete_warehouse(self):
        if self.service is None:
            return

        fields = [
            {"name": "warehouse_id", "label": "ID склада:", "required": True, "value_type": int},
        ]
        self.create_form("Удалить склад", fields, self.submit_delete_warehouse)

    def submit_delete_warehouse(self, warehouse_id: int):
        self.service.remove_warehouse(warehouse_id)
        self.log(f"Склад {warehouse_id} удалён вместе с зависимыми грузами.")
        messagebox.showinfo("Успех", "Склад успешно удалён.")
        self.clear_form()

    def show_warehouses_info(self):
        if self.service is None:
            return
        try:
            summary = self.service.get_warehouses_info()
            if not summary["warehouses"]:
                self.log("Запрошена информация по складам: складов нет.")
                messagebox.showinfo("Информация о складах", "Склады отсутствуют.")
                return

            lines = [
                f"ID={wh['id']} | {wh['name']} | {wh['location']} | загрузка={wh['current_weight']} / {wh['capacity']} тонн | свободно={wh['free_space']} тонн"
                for wh in summary["warehouses"]
            ]
            text = "\n".join(lines)
            self.log(f"Запрошена информация по {len(summary['warehouses'])} складам.")
            messagebox.showinfo("Информация о складах", text)
        except Exception as exc:
            self.show_error("Ошибка информации по складам", exc)


if __name__ == "__main__":
    app = LogisticsGUI()
    app.mainloop()
