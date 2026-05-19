# заполнения тестовыми данными

import sys
from datetime import date, timedelta
from database.orm_repository import ORMRepository
from service.exceptions import DuplicateEntityError, EntityNotFoundError

# URL подключения к вашей базе данных PostgreSQL
DB_URL_ORM = "postgresql://postgres:mysecret@localhost:5432/logistic_db"


def clear_database(repo: ORMRepository):
    """Очищает базу данных перед заполнением, чтобы избежать конфликтов уникальности."""
    print("[Seed] Очистка старых данных перед заполнением...")
    with repo.Session() as session:
        # Удаляем данные в порядке, учитывающем внешние ключи
        session.execute("TRUNCATE TABLE shipment_driver, shipment, driver, warehouse RESTART IDENTITY CASCADE;")
        session.commit()
    print("[Seed] База данных успешно очищена.")


def populate_data():
    repo = ORMRepository(DB_URL_ORM)
    
    try:
        # 0. Очищаем базу для стабильного повторного запуска
        clear_database(repo)
        
        print("\n[Seed] Начинаем заполнение тестовыми данными...")

        # 1. Добавляем ровно 3 склада (Warehouse) — ID передаем вручную!
        warehouses_data = [
            (1, "Главный Терминал А", "Москва, ул. Ленина, д. 10", 1500.0),
            (2, "Региональный Хаб Б", "Санкт-Петербург, Пулковское ш., д. 4", 800.0),
            (3, "Распределительный Центр С", "Новосибирск, ул. Станционная, д. 25", 1200.0)
        ]
        
        warehouse_ids = []
        for w_id, name, loc, cap in warehouses_data:
            inserted_id = repo.add_warehouse(w_id, name, loc, cap)
            warehouse_ids.append(inserted_id)
        print(f" -> Успешно добавлено складов: {len(warehouse_ids)} (ID: {warehouse_ids})")

        # 2. Добавляем ровно 4 водителей (Driver)
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
        print(f" -> Успешно добавлено водителей: {len(driver_ids)} (ID: {driver_ids})")

        # 3. Добавляем ровно 8 грузов (Shipment)
        # Распределяем их по трем созданным складам
        shipments_data = [
            ("TRK-001", 150.5, "На складе", warehouse_ids[0]),
            ("TRK-002", 450.0, "В пути", warehouse_ids[0]),
            ("TRK-003", 85.0, "На складе", warehouse_ids[0]),
            ("TRK-004", 1200.0, "На складе", warehouse_ids[1]),
            ("TRK-005", 310.2, "В пути", warehouse_ids[1]),
            ("TRK-006", 950.0, "На складе", warehouse_ids[2]),
            ("TRK-007", 45.0, "Доставлен", warehouse_ids[2]),
            ("TRK-008", 620.1, "На складе", warehouse_ids[2])
        ]
        
        shipment_ids = []
        for tracking, weight, status, wh_id in shipments_data:
            inserted_id = repo.add_shipment(tracking, weight, status, wh_id)
            shipment_ids.append(inserted_id)
        print(f" -> Успешно добавлено грузов: {len(shipment_ids)} (ID: {shipment_ids})")

        # 4. Добавляем ровно 10 связей назначений (ShipmentDriver)
        # Отражаем, какой водитель доставляет груз и дату доставки
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
        print(f" -> Успешно добавлено связей (доставок): {len(assignment_ids)}")

        print("\n🎉 [Seed] БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА ТЕСТОВЫМИ ДАННЫМИ!")
        print("Все требования по объему данных для Варианта 4 выполнены.")

    except (DuplicateEntityError, EntityNotFoundError) as ex:
        print(f"\n❌ [Seed Ошибка бизнес-логики]: {ex}")
    except Exception as e:
        print(f"\n💥 [Seed Критическая ошибка]: {e}")
        sys.exit(1)


if __name__ == "__main__":
    populate_data()
