import psycopg2
from psycopg2.extras import RealDictCursor
from database.base_repository import BaseRepository
from service.exceptions import (
    DuplicateEntityError, 
    EntityNotFoundError, 
    InvalidStatusError, 
    VALID_STATUSES
)
from typing import List, Dict, Any
from datetime import date

class SQLRepository(BaseRepository):


    def __init__(self, dsn):
        #принимает строку подключения DSN
        self.dsn = dsn

    def _get_connection(self):
        # Использование RealDictCursor заставляет psycopg2 возвращать строки в виде словарей,
        # что гарантирует идентичность структур данных с ORM-репозиторием
        return psycopg2.connect(self.dsn, cursor_factory=RealDictCursor)
    


    def add_warehouse(self, name, location, capacity):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        "select id from warehouse where name = %s and location = %s;", 
                        (name, location)
                    )
                    if cur.fetchone():
                        raise DuplicateEntityError(f"склад '{name}' по адресу '{location}' уже существует")

                    cur.execute(
                        "insert into warehouse (name, location, capacity) values (%s, %s, %s) returning id;",
                        (name, location, capacity)
                    )
                    warehouse_id = cur.fetchone()['id']
                    conn.commit()
                    return warehouse_id
                except (DuplicateEntityError, EntityNotFoundError, InvalidStatusError):
                    raise
                except Exception as e:
                    conn.rollback()
                    raise e


    def add_shipment(self, tracking_number:str, weight: float, status, warehouse_id):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    if status not in VALID_STATUSES:
                        raise InvalidStatusError(
                            f"недопустимый статус груза: '{status}' допустимые значения: {', '.join(VALID_STATUSES)}"
                        )
                    cur.execute("select id from warehouse where id = %s;", (warehouse_id,))
                    if not cur.fetchone():
                        raise EntityNotFoundError(f"склад с ID {warehouse_id} не существует")

                    cur.execute("select id from shipment where tracking_number = %s;", (tracking_number,))
                    if cur.fetchone():
                        raise DuplicateEntityError(f"груз с трек-номером '{tracking_number}' уже добавлен")

                    cur.execute(
                        "insert into shipment (tracking_number, weight, status, warehouse_id) values (%s, %s, %s, %s) returning id;",
                        (tracking_number, weight, status, warehouse_id)
                    )
                    shipment_id = cur.fetchone()['id']
                    conn.commit()
                    return shipment_id
                except (DuplicateEntityError, EntityNotFoundError, InvalidStatusError):
                    raise
                except Exception as e:
                    conn.rollback()
                    raise e

    def add_driver(self, name, license_number):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("select id from driver where license_number = %s;", (license_number,))
                    if cur.fetchone():
                        raise DuplicateEntityError(f"водитель с номером лицензии '{license_number}' уже добавлен")

                    # 2. Вставка записи
                    cur.execute(
                        "insert into driver (name, license_number) values (%s, %s) returning id;",
                        (name, license_number)
                    )
                    driver_id = cur.fetchone()['id']
                    conn.commit()
                    return driver_id
                except (DuplicateEntityError, EntityNotFoundError, InvalidStatusError):
                    raise
                except Exception as e:
                    conn.rollback()
                    raise e

    def add_shipment_driver(self, shipment_id: int, driver_id: int, delivery_date: date) -> int:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("select id from shipment where id = %s;", (shipment_id,))
                    if not cur.fetchone():
                        raise EntityNotFoundError(f"груз с id {shipment_id} не найден")

                    # 2. Проверяем существование водителя
                    cur.execute("select id from driver where id = %s;", (driver_id,))
                    if not cur.fetchone():
                        raise EntityNotFoundError(f"водитель с ID {driver_id} не найден")


                    cur.execute(
                        "select id from shipment_driver where shipment_id = %s and driver_id = %s and delivery_date = %s;",
                        (shipment_id, driver_id, delivery_date)
                    )
                    if cur.fetchone():
                        raise DuplicateEntityError("Этот водитель уже назначен на данный груз на выбранную дату")

                    cur.execute(
                        "insert into shipment_driver (shipment_id, driver_id, delivery_date) values (%s, %s, %s) returning id;",
                        (shipment_id, driver_id, delivery_date)
                    )
                    sd_id = cur.fetchone()['id']
                    conn.commit()
                    return sd_id
                except (DuplicateEntityError, EntityNotFoundError, InvalidStatusError):
                    raise
                except Exception as e:
                    conn.rollback()
                    raise e


    def get_shipments_by_warehouse(self, warehouse_id) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("select id from warehouse where id = %s;", (warehouse_id,))
                    if not cur.fetchone():
                        raise EntityNotFoundError(f"cклад {warehouse_id} не найден")

                    cur.execute(
                        "select id, tracking_number, weight, status, warehouse_id from shipment where warehouse_id = %s;",
                        (warehouse_id,)
                    )
                    # Из-за RealDictCursor элементы списка уже являются словарями. 
                    # Приводим к обычному dict для полной очистки от специфичных типов psycopg2
                    return [dict(row) for row in cur.fetchall()]
                except EntityNotFoundError:
                    raise
                except Exception as e:
                    raise e

    def get_driver_delivery_counts(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    query = """
                        select d.id, d.name, d.license_number, count(sd.id) as delivery_count
                        from driver d
                        left join shipment_driver sd ON d.id = sd.driver_id
                        group by d.id, d.name, d.license_number
                        order by delivery_count DESC;
                    """
                    cur.execute(query)
                    return [dict(row) for row in cur.fetchall()]
                except Exception as e:
                    raise e


    def update_shipment(self, shipment_id, status: str = None, warehouse_id: int = None) -> bool:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("select id from shipment where id = %s;", (shipment_id,))
                    if not cur.fetchone():
                        raise EntityNotFoundError(f"Груз с ID {shipment_id} не найден")

                    fields = []
                    values = []

                    # Если меняется статус — валидируем его
                    if status is not None:
                        if status not in VALID_STATUSES:
                            raise InvalidStatusError(
                                f"Недопустимый статус груза: '{status}'. Разрешенные значения: {', '.join(VALID_STATUSES)}"
                            )
                        fields.append("status = %s")
                        values.append(status)

                    # Если меняется склад
                    if warehouse_id is not None:
                        cur.execute("select id from warehouse where id = %s;", (warehouse_id,))
                        if not cur.fetchone():
                            raise EntityNotFoundError(f"Невозможно переместить груз: склад с ID {warehouse_id} не существует")
                        fields.append("warehouse_id = %s")
                        values.append(warehouse_id)

                    if not fields:
                        return False

                    query = f"update shipment SET {', '.join(fields)} where id = %s;"
                    values.append(shipment_id)

                    cur.execute(query, tuple(values))
                    conn.commit()
                    return True
                except (DuplicateEntityError, EntityNotFoundError, InvalidStatusError):
                    raise
                except Exception as e:
                    conn.rollback()
                    raise e


    def delete_shipment(self, shipment_id) -> bool:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("select id from shipment where id = %s;", (shipment_id,))
                    if not cur.fetchone():
                        raise EntityNotFoundError(f"груз с ID {shipment_id} не найден. Удаление невозможно")

                    cur.execute("delete from shipment where id = %s;", (shipment_id,))
                    conn.commit()
                    return True
                except EntityNotFoundError:
                    raise
                except Exception as e:
                    conn.rollback()
                    raise e

    def delete_warehouse(self, warehouse_id) -> bool:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("select id from warehouse where id = %s;", (warehouse_id,))
                    if not cur.fetchone():
                        raise EntityNotFoundError(f"Склад с ID {warehouse_id} не найден. Удаление невозможно.")

                    # Каскадное удаление грузов 
                    cur.execute("delete from warehouse where id = %s;", (warehouse_id,))
                    conn.commit()
                    return True
                except EntityNotFoundError:
                    raise
                except Exception as e:
                    conn.rollback()
                    raise e

    def get_warehouse_capacity(self, warehouse_id) -> float:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("select capacity from warehouse where id = %s;", (warehouse_id,))
                res = cur.fetchone()
                return res['capacity'] if res else 0.0

    def get_shipment_weight(self, shipment_id) -> float:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("select weight from shipment where id = %s;", (shipment_id,))
                res = cur.fetchone()
                return res['weight'] if res else 0.0

    def get_all_warehouses(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("select id, name, location, capacity from warehouse order by id;")
                return [dict(row) for row in cur.fetchall()]