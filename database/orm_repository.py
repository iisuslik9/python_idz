from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database.base_repository import BaseRepository
from database.orm_models import Warehouse, Shipment, Driver, ShipmentDriver
from typing import List, Dict, Any
from datetime import date
from sqlalchemy.exc import IntegrityError
from service.exceptions import DuplicateEntityError, EntityNotFoundError, VALID_STATUSES, InvalidStatusError

class ORMRepository(BaseRepository):

    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)

    def add_warehouse(self, name, location, capacity):
        with self.Session() as session: #Контекстный менеджер with автоматически закроет сессию после выхода из блока try-except
            try:
                existing_wh = session.query(Warehouse).filter_by(name=name, location=location).first()
                if existing_wh:
                    raise DuplicateEntityError(f"cклад '{name}' по адресу '{location}' уже существует")

                obj = Warehouse(name=name, location=location, capacity=capacity)
                session.add(obj)
                session.commit()
                return obj.id
            except (DuplicateEntityError, EntityNotFoundError):
                raise
            except Exception as e:
                session.rollback()
                raise e

    def add_shipment(self, tracking_number, weight, status, warehouse_id):
        with self.Session() as session:
            try:
                if status not in VALID_STATUSES:
                    raise InvalidStatusError(
                        f"недопустимый статус груза: '{status}'. допустимые значения: {', '.join(VALID_STATUSES)}"
                    )
                
                warehouse = session.query(Warehouse).filter_by(id=warehouse_id).first()
                if not warehouse:
                    raise EntityNotFoundError(f"невозможно добавить груз: склад с ID {warehouse_id} не существует")
                
                existing_shipment = session.query(Shipment).filter_by(tracking_number=tracking_number).first()
                if existing_shipment:
                    raise DuplicateEntityError(f"груз с трек-номером '{tracking_number}' уже зарегистрирован")

                obj = Shipment(tracking_number=tracking_number, weight=weight, status=status, warehouse_id=warehouse_id)
                session.add(obj)
                session.commit()
                return obj.id
            except (DuplicateEntityError, EntityNotFoundError):  # пропускаем кастомные ошибки
                raise
            except Exception as e:
                session.rollback()
                raise e

    def add_driver(self, name, license_number):
        with self.Session() as session:
            try:
                existing_driver = session.query(Driver).filter_by(license_number=license_number).first()
                if existing_driver:
                    raise DuplicateEntityError(f"водитель с номером лицензии '{license_number}' уже есть в бд")

                obj = Driver(name=name, license_number=license_number)
                session.add(obj)
                session.commit()
                return obj.id
            except (DuplicateEntityError, EntityNotFoundError):
                raise
            except Exception as e:
                session.rollback()
                raise e

    def add_shipment_driver(self, shipment_id, driver_id, delivery_date):
        with self.Session() as session:
            try:
                obj = ShipmentDriver(shipment_id=shipment_id, driver_id=driver_id, delivery_date=delivery_date)
                session.add(obj)
                session.commit()
                return obj.id
            except IntegrityError as e:
                session.rollback()
                if "shipment_id" in str(e.orig):
                    raise EntityNotFoundError(f"ошибка назначения: груз с ID {shipment_id} не найден")
                if "driver_id" in str(e.orig):
                    raise EntityNotFoundError(f"ошибка назначения: водитель с ID {driver_id} не найден")
                raise e


    def get_shipments_by_warehouse(self, warehouse_id):
        with self.Session() as session:
            try:
                warehouse = session.query(Warehouse).filter_by(id=warehouse_id).first()
                if not warehouse:
                    raise EntityNotFoundError(f"склад с ID {warehouse_id} не найден")
                    
                shipments = session.query(Shipment).filter(Shipment.warehouse_id == warehouse_id).all()
                #list[dict{string: any}]
                return [
                    {
                        "id": s.id,
                        "tracking_number": s.tracking_number,
                        "weight": s.weight,
                        "status": s.status,
                        "warehouse_id": s.warehouse_id
                    } for s in shipments
                ]
            except EntityNotFoundError:
                raise
            except Exception as e:
                raise e

    def get_driver_delivery_counts(self):
        with self.Session() as session:
            try:
                results = session.query(
                    Driver.id,
                    Driver.name,
                    Driver.license_number,
                    func.count(ShipmentDriver.id).label("delivery_count")
                ).outerjoin(ShipmentDriver, Driver.id == ShipmentDriver.driver_id)\
                 .group_by(Driver.id, Driver.name, Driver.license_number)\
                 .order_by(func.count(ShipmentDriver.id).desc())\
                 .all()
                
                return [
                    {
                        "id": r.id,
                        "name": r.name,
                        "license_number": r.license_number,
                        "delivery_count": r.delivery_count
                    } for r in results
                ]
            except Exception as e:
                raise e


    def update_shipment(self, shipment_id, status: str = None, warehouse_id: int = None):
        with self.Session() as session:
            try:
                shipment = session.query(Shipment).filter_by(id=shipment_id).first()
                if not shipment:
                    raise EntityNotFoundError(f"груз с ID {shipment_id} не найден")
                
                if status is not None:
                    if status not in VALID_STATUSES:
                        raise InvalidStatusError(
                            f"недопустимый статус груза: '{status}'. допустимые значения: {', '.join(VALID_STATUSES)}"
                        )
                    shipment.status = status
                
                if warehouse_id is not None:
                    target_warehouse = session.query(Warehouse).filter_by(id=warehouse_id).first()
                    if not target_warehouse:
                        raise EntityNotFoundError(f"склад с ID {warehouse_id} не существует")
                    shipment.warehouse_id = warehouse_id
                    
                if status is not None:
                    shipment.status = status
                    
                session.commit()
                return True
            except (DuplicateEntityError, EntityNotFoundError):
                raise
            except Exception as e:
                session.rollback()
                raise e


    def delete_shipment(self, shipment_id):
        with self.Session() as session:
            try:
                shipment = session.query(Shipment).filter_by(id=shipment_id).first()
                if not shipment:
                    raise EntityNotFoundError(f"груз с ID {shipment_id} не найден")
                    
                session.delete(shipment)
                session.commit()
                return True
            except EntityNotFoundError:
                raise
            except Exception as e:
                session.rollback()
                raise e

    def delete_warehouse(self, warehouse_id):
        with self.Session() as session:
            try:
                warehouse = session.query(Warehouse).filter_by(id=warehouse_id).first()
                if not warehouse:
                    raise EntityNotFoundError(f"Склад с ID {warehouse_id} не найден. Удаление невозможно.")
                    
                session.delete(warehouse)
                session.commit()
                return True
            except EntityNotFoundError:
                raise
            except Exception as e:
                session.rollback()
                raise e

    def get_warehouse_capacity(self, warehouse_id) -> float:
        with self.Session() as session:
            warehouse = session.query(Warehouse).filter_by(id=warehouse_id).first()
            return warehouse.capacity if warehouse else 0.0

    def get_shipment_weight(self, shipment_id) -> float:
        with self.Session() as session:
            shipment = session.query(Shipment).filter_by(id=shipment_id).first()
            return shipment.weight if shipment else 0.0
        
    def get_all_warehouses(self) -> List[Dict[str, Any]]:
        with self.Session() as session:
            warehouses = session.query(Warehouse).order_by(Warehouse.id).all()
            return [
                {"id": w.id, "name": w.name, "location": w.location, "capacity": w.capacity}
                for w in warehouses
            ]

