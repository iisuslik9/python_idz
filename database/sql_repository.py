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


    def __init__(self, dsn: str):
        """Принимает строку подключения DSN, например: 
        "host=localhost dbname=logistic_db user=postgres password=mysecret"
        """
        self.dsn = dsn

    def _get_connection(self):
        # Использование RealDictCursor заставляет psycopg2 возвращать строки в виде словарей,
        # что гарантирует идентичность структур данных с ORM-репозиторием.
        return psycopg2.connect(self.dsn, cursor_factory=RealDictCursor)

    # ==========================================
    # МЕТОДЫ ДОБАВЛЕНИЯ ЗАПИСЕЙ В ТАБЛИЦЫ
    # ==========================================
    def add_warehouse(self, name: str, location: str, capacity: float) -> int:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    # 1. Проверяем дубликат склада по имени и адресу
                    cur.execute(
                        "SELECT id FROM warehouse WHERE name = %s AND location = %s;", 
                        (name, location)
                    )
                    if cur.fetchone():
                        raise DuplicateEntityError(f"Склад '{name}' по адресу '{location}' уже существует.")

                    # 2. Вставка записи
                    cur.execute(
                        "INSERT INTO warehouse (name, location, capacity) VALUES (%s, %s, %s) RETURNING id;",
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


    def add_shipment(self, tracking_number: str, weight: float, status: str, warehouse_id: int) -> int:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    # 1. Валидация статуса
                    if status not in VALID_STATUSES:
                        raise InvalidStatusError(
                            f"Недопустимый статус груза: '{status}'. Разрешенные значения: {', '.join(VALID_STATUSES)}"
                        )

                    # 2. Проверяем, существует ли целевой склад
                    cur.execute("SELECT id FROM warehouse WHERE id = %s;", (warehouse_id,))
                    if not cur.fetchone():
                        raise EntityNotFoundError(f"Невозможно добавить груз: склад с ID {warehouse_id} не существует.")

                    # 3. Проверяем уникальность трек-номера
                    cur.execute("SELECT id FROM shipment WHERE tracking_number = %s;", (tracking_number,))
                    if cur.fetchone():
                        raise DuplicateEntityError(f"Груз с трек-номером '{tracking_number}' уже зарегистрирован.")

                    # 4. Вставка записи
                    cur.execute(
                        """INSERT INTO shipment (tracking_number, weight, status, warehouse_id) 
                           VALUES (%s, %s, %s, %s) RETURNING id;""",
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

    def add_driver(self, name: str, license_number: str) -> int:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    # 1. Проверяем уникальность лицензии
                    cur.execute("SELECT id FROM driver WHERE license_number = %s;", (license_number,))
                    if cur.fetchone():
                        raise DuplicateEntityError(f"Водитель с номером лицензии '{license_number}' уже есть в базе.")

                    # 2. Вставка записи
                    cur.execute(
                        "INSERT INTO driver (name, license_number) VALUES (%s, %s) RETURNING id;",
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
                    # 1. Проверяем существование груза
                    cur.execute("SELECT id FROM shipment WHERE id = %s;", (shipment_id,))
                    if not cur.fetchone():
                        raise EntityNotFoundError(f"Ошибка назначения: груз с ID {shipment_id} не найден.")

                    # 2. Проверяем существование водителя
                    cur.execute("SELECT id FROM driver WHERE id = %s;", (driver_id,))
                    if not cur.fetchone():
                        raise EntityNotFoundError(f"Ошибка назначения: водитель с ID {driver_id} не найден.")

                    # 3. Проверяем дубликат назначения на конкретную дату
                    cur.execute(
                        """SELECT id FROM shipment_driver 
                           WHERE shipment_id = %s AND driver_id = %s AND delivery_date = %s;""",
                        (shipment_id, driver_id, delivery_date)
                    )
                    if cur.fetchone():
                        raise DuplicateEntityError("Этот водитель уже назначен на данный груз на выбранную дату.")

                    # 4. Вставка записи
                    cur.execute(
                        """INSERT INTO shipment_driver (shipment_id, driver_id, delivery_date) 
                           VALUES (%s, %s, %s) RETURNING id;""",
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

    # ==========================================
    # ВЫБОРКА И АНАЛИТИКА
    # ==========================================

    def get_shipments_by_warehouse(self, warehouse_id: int) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    # Проверяем существование склада
                    cur.execute("SELECT id FROM warehouse WHERE id = %s;", (warehouse_id,))
                    if not cur.fetchone():
                        raise EntityNotFoundError(f"Склад с ID {warehouse_id} не найден.")

                    cur.execute(
                        "SELECT id, tracking_number, weight, status, warehouse_id FROM shipment WHERE warehouse_id = %s;",
                        (warehouse_id,)
                    )
                    # Из-за RealDictCursor элементы списка уже являются словарями. 
                    # Приводим к обычному dict для полной очистки от специфичных типов psycopg2.
                    return [dict(row) for row in cur.fetchall()]
                except EntityNotFoundError:
                    raise
                except Exception as e:
                    raise e

    def get_driver_delivery_counts(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    # Пишем сырой LEFT JOIN с агрегацией COUNT и группировкой GROUP BY
                    query = """
                        SELECT d.id, d.name, d.license_number, COUNT(sd.id) as delivery_count
                        FROM driver d
                        LEFT JOIN shipment_driver sd ON d.id = sd.driver_id
                        GROUP BY d.id, d.name, d.license_number
                        ORDER BY delivery_count DESC;
                    """
                    cur.execute(query)
                    return [dict(row) for row in cur.fetchall()]
                except Exception as e:
                    raise e

    # ==========================================
    # МЕТОДЫ ОБНОВЛЕНИЯ ДАННЫХ
    # ==========================================

    def update_shipment(self, shipment_id: int, status: str = None, warehouse_id: int = None) -> bool:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    # 1. Проверяем существование груза
                    cur.execute("SELECT id FROM shipment WHERE id = %s;", (shipment_id,))
                    if not cur.fetchone():
                        raise EntityNotFoundError(f"Груз с ID {shipment_id} не найден для обновления.")

                    fields = []
                    values = []

                    # 2. Если меняется статус — валидируем его
                    if status is not None:
                        if status not in VALID_STATUSES:
                            raise InvalidStatusError(
                                f"Недопустимый статус груза: '{status}'. Разрешенные значения: {', '.join(VALID_STATUSES)}"
                            )
                        fields.append("status = %s")
                        values.append(status)

                    # 3. Если меняется склад — проверяем его наличие в системе
                    if warehouse_id is not None:
                        cur.execute("SELECT id FROM warehouse WHERE id = %s;", (warehouse_id,))
                        if not cur.fetchone():
                            raise EntityNotFoundError(f"Невозможно переместить груз: целевой склад с ID {warehouse_id} не существует.")
                        fields.append("warehouse_id = %s")
                        values.append(warehouse_id)

                    if not fields:
                        return False

                    # Собираем динамический SQL-запрос обновления
                    query = f"UPDATE shipment SET {', '.join(fields)} WHERE id = %s;"
                    values.append(shipment_id)

                    cur.execute(query, tuple(values))
                    conn.commit()
                    return True
                except (DuplicateEntityError, EntityNotFoundError, InvalidStatusError):
                    raise
                except Exception as e:
                    conn.rollback()
                    raise e

    # ==========================================
    # МЕТОДЫ УДАЛЕНИЯ
    # ==========================================

    def delete_shipment(self, shipment_id: int) -> bool:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("SELECT id FROM shipment WHERE id = %s;", (shipment_id,))
                    if not cur.fetchone():
                        raise EntityNotFoundError(f"Груз с ID {shipment_id} не найден. Удаление невозможно.")

                    cur.execute("DELETE FROM shipment WHERE id = %s;", (shipment_id,))
                    conn.commit()
                    return True
                except EntityNotFoundError:
                    raise
                except Exception as e:
                    conn.rollback()
                    raise e

    def delete_warehouse(self, warehouse_id: int) -> bool:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("SELECT id FROM warehouse WHERE id = %s;", (warehouse_id,))
                    if not cur.fetchone():
                        raise EntityNotFoundError(f"Склад с ID {warehouse_id} не найден. Удаление невозможно.")

                    # Каскадное удаление грузов произойдет на уровне СУБД, так как в схеме 
                    # таблиц (в миграциях) мы пропишем FOREIGN KEY ... ON DELETE CASCADE.
                    cur.execute("DELETE FROM warehouse WHERE id = %s;", (warehouse_id,))
                    conn.commit()
                    return True
                except EntityNotFoundError:
                    raise
                except Exception as e:
                    conn.rollback()
                    raise e

    def get_warehouse_capacity(self, warehouse_id: int) -> float:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT capacity FROM warehouse WHERE id = %s;", (warehouse_id,))
                res = cur.fetchone()
                return res['capacity'] if res else 0.0

    def get_shipment_weight(self, shipment_id: int) -> float:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT weight FROM shipment WHERE id = %s;", (shipment_id,))
                res = cur.fetchone()
                return res['weight'] if res else 0.0
