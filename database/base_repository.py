# Через SQLAlchemy ORM и через прямые SQL-запросы с использованием
# DB API 2.0 реализуйте следующие операции:
# • Методы добавления записей в таблицы (Warehouse, Shipment, Driver,
# ShipmentDriver). 
# • Метод выборки всех грузов на определённом складе.
# • Функцию добавления записи о назначении водителя на доставку груза.
# • Методы обновления данных о грузе (например, изменение статуса или
# склада).
# • Методы удаления груза или склада.
# • Метод вычисления общего количества доставок, выполненных каждым
# водителем.

from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def add_warehouse(self, warehouse_id, name, location, capacity): 
        pass

    @abstractmethod
    def add_shipment(self, tracking_number, weight, status, warehouse_id): 
        pass

    @abstractmethod
    def add_driver(self, name, license_number): 
        pass

    @abstractmethod
    def add_shipment_driver(self, shipment_id, driver_id, delivery_date): 
        pass



    @abstractmethod
    def get_shipments_by_warehouse(self, warehouse_id): 
        pass




    @abstractmethod
    def update_shipment(self, shipment_id, status=None, warehouse_id=None): 
        pass

    @abstractmethod
    def delete_shipment(self, shipment_id): 
        pass

    @abstractmethod
    def delete_warehouse(self, warehouse_id):
        pass

    @abstractmethod
    def get_driver_delivery_counts(self):
        pass


    @abstractmethod
    def get_warehouse_capacity(self, warehouse_id):
        pass

    @abstractmethod
    def get_shipment_weight(self, shipment_id):
        pass

    @abstractmethod
    def get_all_warehouses(self):
        """Возвращает список всех зарегистрированных складов."""
        pass