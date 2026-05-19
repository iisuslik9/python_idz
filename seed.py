# заполнения тестовыми данными
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATABASE_URL
from datetime import date, timedelta
from database.orm_repository import ORMRepository
from service.exceptions import DuplicateEntityError, EntityNotFoundError
from sqlalchemy import text


def clear_database(repo: ORMRepository):
    print("[Seed] Очистка старых данных перед заполнением...")
    with repo.Session() as session:
        session.execute(text("TRUNCATE TABLE shipment_driver, shipment, driver, warehouse RESTART IDENTITY CASCADE;"))
        session.commit()
    print("[Seed] База данных успешно очищена.")


def populate_data():
    repo = ORMRepository(DATABASE_URL)
    
    try:
        clear_database(repo)
        
        print("\n[Seed] Начинаем заполнение тестовыми данными...")

        warehouses_data = [
            ("Главный Терминал А", "Москва, ул. Ленина, д. 10", 15.0),
            ("Региональный Хаб Б", "Санкт-Петербург, Пулковское ш., д. 4", 8.0),
            ("Распределительный Центр С", "Новосибирск, ул. Станционная, д. 25", 12.0)
        ]
        
        warehouse_ids = []
        for name, loc, cap in warehouses_data:
            inserted_id = repo.add_warehouse(name, loc, cap)
            warehouse_ids.append(inserted_id)


        drivers_data = [
            ("Иванов Иван Иванович", "77АА123456"),
            ("Петров Петр Петрович", "78ББ654321"),
            ("Сидоров Алексей Николаевич", "54СС987654"),
            ("Козлов Дмитрий Сергеевич", "50ДД456123")
        ]
        
        driver_ids = []
        for name, license_num in drivers_data:
            inserted_id = repo.add_driver(name, license_num)
            driver_ids.append(inserted_id)


        shipments_data = [
            ("TRK-001", 6000, "на складе", warehouse_ids[0]),
            ("TRK-002", 4500.0, "в пути", warehouse_ids[0]),
            ("TRK-003", 7500.0, "на складе", warehouse_ids[0]),
            ("TRK-004", 1200.0, "на складе", warehouse_ids[1]),
            ("TRK-005", 3100.2, "в пути", warehouse_ids[1]),
            ("TRK-006", 9500.0, "на складе", warehouse_ids[2]),
            ("TRK-007", 4500.0, "доставлен", warehouse_ids[2]),
            ("TRK-008", 1000.0, "на складе", warehouse_ids[2])
        ]
        
        shipment_ids = []
        for tracking, weight, status, wh_id in shipments_data:
            inserted_id = repo.add_shipment(tracking, weight, status, wh_id)
            shipment_ids.append(inserted_id)


        today = date.today()
        assignments_data = [
            (shipment_ids[0], driver_ids[0], today),                 # Водитель 1 везет груз 1 сегодня
            (shipment_ids[1], driver_ids[0], today + timedelta(days=1)), # Водитель 1 везет груз 2 завтра
            (shipment_ids[2], driver_ids[1], today),                 # Водитель 2 везет груз 3 сегодня
            (shipment_ids[3], driver_ids[1], today - timedelta(days=1)), # Водитель 2 везет груз 4 вчера
            (shipment_ids[4], driver_ids[2], today),                 # Водитель 3 везет груз 5 сегодня
            (shipment_ids[5], driver_ids[2], today + timedelta(days=2)), # Водитель 3 везет груз 6 послезавтра
            (shipment_ids[6], driver_ids[3], today - timedelta(days=2)), # Водитель 4 везет груз 7 два дня назад
            (shipment_ids[7], driver_ids[3], today),                 # Водитель 4 везет груз 8 сегодня
            (shipment_ids[0], driver_ids[3], today + timedelta(days=3)), # Водитель 4 везет груз 1 через 3 дня (повторная доставка)
            (shipment_ids[1], driver_ids[2], today - timedelta(days=3))  # Водитель 3 везет груз 2 три дня назад
        ]
        
        assignment_ids = []
        for s_id, d_id, d_date in assignments_data:
            inserted_id = repo.add_shipment_driver(s_id, d_id, d_date)
            assignment_ids.append(inserted_id)


        print("\БД УСПЕШНО ЗАПОЛНЕНА ТЕСТОВЫМИ ДАННЫМИ")

    except (DuplicateEntityError, EntityNotFoundError) as ex:
        print(f" [Seed Ошибка бизнес-логики]: {ex}")
    except Exception as e:
        print(f"[Seed Критическая ошибка]: {e}")
        sys.exit(1)


if __name__ == "__main__":
    populate_data()
