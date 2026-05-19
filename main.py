import sys
from datetime import datetime

# Импорт слоев данных и логики
from database.sql_repository import SQLRepository
from database.orm_repository import ORMRepository
from service.logistics_service import LogisticsService
from service.exceptions import (
    DuplicateEntityError, 
    EntityNotFoundError, 
    InvalidStatusError,
    VALID_STATUSES,
    WarehouseCapacityExceededError
)

# =====================================================================
# НАСТРОЙКИ ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ
# =====================================================================
DB_DSN_SQL = "host=localhost dbname=logistic_company user=postgres password=1 port=5433"
DB_URL_ORM = "postgresql://postgres:1@localhost:5433/logistic_company"


def choose_database_mode():
    """Запрашивает у пользователя режим работы с базой данных."""
    while True:
        print("===========================================================")
        print("===           СИСТЕМА УПРАВЛЕНИЯ ЛОГИСТИКОЙ             ===")
        print("===========================================================")
        print("Выберите режим работы с базой данных:")
        print("1 — Чистый SQL (Использование Python DB-API 2.0 / psycopg2)")
        print("2 — ORM-модели (Использование SQLAlchemy ORM)")
        print("0 — Выход из приложения")
        print("===========================================================")
        
        choice = input("Введите цифру: ").strip()
        
        if choice == "1":
            print("\n[Система] Инициализация... Выбран режим: SQL.\n")
            return SQLRepository(DB_DSN_SQL)
        elif choice == "2":
            print("\n[Система] Инициализация... Выбран режим: SQLAlchemy ORM.\n")
            return ORMRepository(DB_URL_ORM)
        elif choice == "0":
            print("Завершение работы приложения.")
            sys.exit()
        else:
            print("❌ Неверный ввод! Пожалуйста, введите 1, 2 или 0.\n")


def run_console_ui(service: LogisticsService):
    """Главный цикл консольного интерфейса (Слой UI)."""
    while True:
        print("\n==================== МЕНЮ ОПЕРАЦИЙ ====================")
        print("1. Добавить склад (Warehouse)")
        print("2. Добавить груз (Shipment)")
        print("3. Добавить водителя (Driver)")
        print("4. Назначить водителя на доставку груза (ShipmentDriver)")
        print("5. Показать все грузы на определённом складе")
        print("6. Обновить данные о грузе (статус и/или склад)")
        print("7. Посчитать общее количество доставок каждого водителя")
        print("8. Удалить груз")
        print("9. Удалить склад")
        print("0. Выход назад в меню выбора режима БД")
        print("=======================================================")
        
        choice = input("Выберите действие (0-9): ").strip()
        
        try:
            # 1. ДОБАВИТЬ СКЛАД
            if choice == "1":
                name = input("Введите название склада: ").strip()
                location = input("Введите адрес склада: ").strip()
                capacity = float(input("Введите общую вместимость склада (тонн): "))
                
                # Вызов строго через метод сервиса
                res_id = service.register_new_warehouse(name, location, capacity)
                print(f"✅ [УСПЕХ]: Склад успешно создан. Присвоен ID: {res_id}")
                
            # 2. ДОБАВИТЬ ГРУЗ
            elif choice == "2":
                tracking = input("Введите уникальный трек-номер груза: ").strip()
                weight = float(input("Введите вес груза (кг): "))
                print(f"Доступные статусы: {', '.join(VALID_STATUSES)}")
                status = input("Введите статус груза: ").strip()
                wh_id = int(input("Введите ID склада, на котором находится груз: "))
                
                # Вызов строго через метод сервиса
                res_id = service.register_new_shipment(tracking, weight, status, wh_id)
                print(f"✅ [УСПЕХ]: Груз зарегистрирован в системе. Присвоен ID: {res_id}")
                
            # 3. ДОБАВИТЬ ВОДИТЕЛЯ
            elif choice == "3":
                name = input("Введите ФИО водителя: ").strip()
                license_num = input("Введите уникальный номер водительской лицензии: ").strip()
                
                # Вызов строго через метод сервиса
                res_id = service.register_new_driver(name, license_num)
                print(f"✅ [УСПЕХ]: Водитель успешно добавлен. Присвоен ID: {res_id}")
                
            # 4. НАЗНАЧИТЬ ВОДИТЕЛЯ НА ДОСТАВКУ
            elif choice == "4":
                shipment_id = int(input("Введите ID груза: "))
                driver_id = int(input("Введите ID водителя: "))
                date_str = input("Введите дату доставки (ГГГГ-ММ-ДД) или нажмите Enter для текущей: ").strip()
                
                if date_str:
                    delivery_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                else:
                    delivery_date = datetime.now().date()
                    
                # Вызов строго через метод сервиса
                res_id = service.assign_driver_to_shipment(shipment_id, driver_id, delivery_date)
                print(f"✅ [УСПЕХ]: Назначение выполнено. ID записи доставки: {res_id}")
                
            # 5. ПОКАЗАТЬ ГРУЗЫ НА СКЛАДЕ
            elif choice == "5":
                wh_id = int(input("Введите ID склада для вывода списка грузов: "))
                
                # Вызов строго через метод сервиса
                shipments = service.get_warehouse_inventory(wh_id)
                
                if not shipments:
                    print(f"ℹ️ На складе №{wh_id} в данный момент нет ни одного груза.")
                else:
                    print(f"\n--- СПИСОК ГРУЗОВ НА СКЛАДЕ №{wh_id} ---")
                    for s in shipments:
                        print(f"ID: {s['id']} | Трек: {s['tracking_number']} | Вес: {s['weight']} кг | Статус: {s['status']}")
            
            # 6. ОБНОВИТЬ ДАННЫЕ О ГРУЗЕ
            elif choice == "6":
                shipment_id = int(input("Введите ID груза, данные которого нужно изменить: "))
                print("--- Оставьте поле пустым (нажмите Enter), если менять его не нужно ---")
                
                new_status = input(f"Новый статус ({'/'.join(VALID_STATUSES)}): ").strip() or None
                
                new_wh_str = input("Новый ID склада для перемещения: ").strip()
                new_wh_id = int(new_wh_str) if new_wh_str else None
                
                if new_status is None and new_wh_id is None:
                    print("⚠️ Ни одного поля для изменения не введено. Операция отменена.")
                    continue
                    
                # Вызов строго через метод сервиса
                service.modify_shipment(shipment_id, status=new_status, warehouse_id=new_wh_id)
                print("✅ [УСПЕХ]: Данные о грузе успешно обновлены.")
                
            # 7. ПОСЧИТАТЬ КОЛИЧЕСТВО ДОСТАВОК ВОДИТЕЛЕЙ
            elif choice == "7":
                # Вызов строго через метод сервиса
                counts = service.get_driver_rankings()
                
                if not counts:
                    print("ℹ️ В базе данных пока нет зарегистрированных водителей.")
                else:
                    print("\n--- ОТЧЕТ: КОЛИЧЕСТВО ДОСТАВОК ПО ВОДИТЕЛЯМ ---")
                    for item in counts:
                        print(f"Водитель (ID: {item['id']}): {item['name']} | Лицензия: {item['license_number']} | Доставок: {item['delivery_count']}")
                    print("------------------------------------------------")
                    
            # 8. УДАЛИТЬ ГРУЗ
            elif choice == "8":
                shipment_id = int(input("Введите ID груза для удаления из системы: "))
                
                # Вызов строго через метод сервиса
                service.remove_shipment(shipment_id)
                print("✅ [УСПЕХ]: Груз окончательно удален из базы данных.")
                
            # 9. УДАЛИТЬ СКЛАД
            elif choice == "9":
                wh_id = int(input("Введите ID склада для удаления: "))
                confirm = input("⚠️ ВНИМАНИЕ! Удаление склада удалит ВСЕ находящиеся на нем грузы (каскадно). Продолжить? (y/n): ")
                
                if confirm.lower() == 'y':
                    # Вызов строго через метод сервиса
                    service.remove_warehouse(wh_id)
                    print("✅ [УСПЕХ]: Склад и все связанные с ним грузы успешно удалены.")
                else:
                    print("❌ Операция отменена пользователем.")
                    
            # 0. ВЫХОД ИЗ ТЕКУЩЕГО РЕЖИМА
            elif choice == "0":
                print("[Система] Выход из текущего режима работы с БД...\n")
                break
            else:
                print("❌ Неизвестная команда! Выберите пункт от 0 до 9.")
                
        # Блоки безопасного перехвата бизнес-ошибок и ошибок валидации
        except DuplicateEntityError as dee:
            print(f"\n⚠️ [ОШИБКА ДУБЛИРОВАНИЯ ДАННЫХ]: {dee}")
        except EntityNotFoundError as enfe:
            print(f"\n❌ [ОШИБКА ДОСТУПА]: {enfe}")
        except InvalidStatusError as ise:
            print(f"\n🛑 [ОШИБКА ВАЛИДАЦИИ СТАТУСА]: {ise}")
        except ValueError as ve:
            print(f"\n🛑 [ОШИБКА ВВОДА]: Неверный формат данных (текст вместо числа или пустая строка). Описание: {ve}")
        except Exception as e:
            print(f"\n💥 [КРИТИЧЕСКАЯ СИСТЕМНАЯ ОШИБКА]: {e}")
        except WarehouseCapacityExceededError as wcee:
            print(f"\n🛑 [ПРЕВЫШЕН ЛИМИТ СКЛАДА]: {wcee}")


if __name__ == "__main__":
    while True:
        # 1. UI-слой запрашивает у пользователя режим работы с БД и создает нужный репозиторий
        chosen_repository = choose_database_mode()
        
        # 2. Инициализируем сервисный слой бизнес-логики и внедряем зависимость (Dependency Injection)
        logistics_service = LogisticsService(repository=chosen_repository)
        
        # 3. Запускаем консольный интерфейс для выбранного режима
        run_console_ui(logistics_service)
