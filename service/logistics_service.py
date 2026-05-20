#бизнес-правила
#валидация
#изоляция интефейса от прямого обращения к репозиториям данных
from datetime import date
from database.base_repository import BaseRepository
from service.exceptions import VALID_STATUSES, InvalidStatusError, WarehouseCapacityExceededError, EntityNotFoundError

class LogisticsService:

    
    def __init__(self, repository: BaseRepository):
        #(Dependency Injection). Принимает любой репозиторий, реализующий интерфейс BaseRepository
        self.repository = repository

    def register_new_warehouse(self, name, location, capacity: float):
        if not name.strip():
            raise ValueError("название склада не может быть пустым")
        if not location.strip():
            raise ValueError("aдрес склада не может быть пустым")
        if capacity <= 0:
            raise ValueError("вместимость склада должна быть > 0")
            
        return self.repository.add_warehouse(name.strip(), location.strip(), capacity)

    def register_new_shipment(self, tracking_number: str, weight: float, status: str, warehouse_id: int) -> int:
        if not tracking_number.strip():
            raise ValueError("tracking_number груза не может быть пустым")
        if weight <= 0:
            raise ValueError("вес груза должен быть > 0")
        if status not in VALID_STATUSES:
            raise InvalidStatusError(
                f"недопустимый статус: '{status}' допустимые: {', '.join(VALID_STATUSES)}"
            )
        

        warehouse_capacity = self.repository.get_warehouse_capacity(warehouse_id)
        if warehouse_capacity == 0.0:
            raise EntityNotFoundError(f"Склад с ID {warehouse_id} не найден.")

        current_shipments = self.repository.get_shipments_by_warehouse(warehouse_id)
        current_total_weight = sum(s['weight'] for s in current_shipments if s['status'] == "на складе") / 1000.0

        if current_total_weight + weight > warehouse_capacity * 1000.0:
            raise WarehouseCapacityExceededError(
                f"Невозможно добавить груз весом {weight} кг. Лимит склада превышен"
                f"Текущая загрузка: {current_total_weight}/{warehouse_capacity} тонн"
            )
            
        return self.repository.add_shipment(tracking_number.strip(), weight, status, warehouse_id)

    def register_new_driver(self, name: str, license_number: str) -> int:
        if not name.strip():
            raise ValueError("ФИО водителя не может быть пустым")
        if not license_number.strip():
            raise ValueError("номер лицензии не может быть пустым")
            
        return self.repository.add_driver(name.strip(), license_number.strip())

    def assign_driver_to_shipment(self, shipment_id, driver_id, delivery_date):
        if shipment_id <= 0 or driver_id <= 0:
            raise ValueError("id груза и id водителя должны быть положительными числами")
        if not isinstance(delivery_date, date):
            raise ValueError("Передан некорректный формат даты")
            
        return self.repository.add_shipment_driver(shipment_id, driver_id, delivery_date)

    def get_warehouse_inventory(self, warehouse_id: int):
        if warehouse_id <= 0:
            raise ValueError("id склада должен быть положительным числом")
            
        return self.repository.get_shipments_by_warehouse(warehouse_id)

    def get_driver_rankings(self):
        return self.repository.get_driver_delivery_counts()

    def modify_shipment(self, shipment_id: int, status: str = None, warehouse_id: int = None) -> bool:

        if shipment_id <= 0:
            raise ValueError("id груза должен быть положительным числом")
        
        if status is not None and status not in VALID_STATUSES:
            raise InvalidStatusError(
                f"Недопустимый статус: '{status}'. Допустимые: {', '.join(VALID_STATUSES)}"
            )


        if warehouse_id is not None:
            if warehouse_id <= 0:
                raise ValueError("id склада должен быть положительным числом.")

            warehouse_capacity = self.repository.get_warehouse_capacity(warehouse_id)
            if warehouse_capacity == 0.0:
                raise EntityNotFoundError(f"cклад с ID {warehouse_id} не найден")

            shipment_weight = self.repository.get_shipment_weight(shipment_id)
            if shipment_weight == 0.0:
                raise EntityNotFoundError(f"груз с ID {shipment_id} не найден")

            # вес грузов на целевом складе
            current_shipments = self.repository.get_shipments_by_warehouse(warehouse_id)
            current_total_weight = sum(s['weight'] for s in current_shipments if s['status'] == "на складе") / 1000.0

           
            if current_total_weight + shipment_weight > warehouse_capacity:
                raise WarehouseCapacityExceededError(
                    f"Невозможно переместить груз. На складе{warehouse_id} недостаточно места"
                    f"(Текущий вес: {current_total_weight} + Вес груза: {shipment_weight} > Лимит: {warehouse_capacity})."
                )

            
        return self.repository.update_shipment(shipment_id, status, warehouse_id)

    def remove_shipment(self, shipment_id) -> bool:
        if shipment_id <= 0:
            raise ValueError("id груза должен быть положительным числом.")
            
        return self.repository.delete_shipment(shipment_id)

    def remove_warehouse(self, warehouse_id) -> bool:
        if warehouse_id <= 0:
            raise ValueError("Идентификатор склада должен быть положительным числом.")
            
        return self.repository.delete_warehouse(warehouse_id)
    
    def get_warehouses_info(self):
        warehouses = self.repository.get_all_warehouses()
        
        # Для каждого склада динамически рассчитываем текущий физический вес грузов
        for wh in warehouses:
            current_shipments = self.repository.get_shipments_by_warehouse(wh['id'])
            current_total_weight = sum(s['weight'] for s in current_shipments if s['status'] == "на складе") / 1000.0
            wh['current_weight'] = current_total_weight
            wh['free_space'] = wh['capacity'] - current_total_weight

        return {
            "warehouses": warehouses
        }
