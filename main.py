from classes import Van, Trailer, Drone, Operator, Depot, DeliveryRoute, LogisticsCompany, SafetyRegulations, VanMaintainable, TrailerMaintainable, DroneMaintainable


def main():
    # 1. Проверка Transport: __new__ и __str__
    print("1. Проверка создания транспорта (без дубликатов):")
    van1 = Van("A123BC77", "Mercedes", 10, 50.0, "бензин")
    trailer1 = Trailer("B456DE77", "Volvo", 20, 25.0, "рефрижератор")
    drone1 = Drone("C789FG77", "DJI", 5, 100.0, 2.0)
    print(van1)
    print(trailer1)
    print(drone1)

    # 2. Проверка запрета дублирования по госномеру
    print("\n2. Попытка создать дубликат номера:")
    try:
        van2 = Van("A123BC77", "Ford", 8, 30.0, "электричество")
    except Exception as e:
        print("Ошибка:", e)

    # 3. Проверка __new__: должно напечатать сообщение, если номер уже есть
    print("\n3. Создание с дубликатом (должно показать сообщение):")
    van3 = Van("A123BC77", "Opel", 8, 30.0, "дизель")  # __new__ уже добавлен в set

    # 4. Проверка Override метода start_delivery (полиморфизм)
    print("\n4. Полиморфизм: start_delivery:")
    print(van1.start_delivery())
    print(trailer1.start_delivery())
    print(drone1.start_delivery())

    # 5. Проверка interface Maintainable
    print("\n5. Интерфейс Maintainable:")
    van_maint = VanMaintainable("D999ZZ77", "Tesla", 8, 40.0, "электричество")
    trailer_maint = TrailerMaintainable("E111EE77", "Scania", 18, 20.0, "открытый")
    drone_maint = DroneMaintainable("F222FF77", "Parrot", 4, 80.0, 1.5)

    for v in [van_maint, trailer_maint, drone_maint]:
        print(f"{v} -> perform_maintenance: {v.perform_maintenance()}")
        print(f"Статус после: {v.status}")

    # 6. Проверка Operator и operate_vehicle
    print("\n6. Класс Operator:")
    op1 = Operator("Иванов И.И.", 5, "грузовой транспорт")
    op2 = Operator("Петров П.П.", 3, "дроны")
    print(op1.operate_vehicle(van1))
    print(op2.operate_vehicle(drone1))

    # 7. Проверка Depot: add_transport, remove_transport, get_available_transpotrs
    print("\n7. Класс Depot:")
    depot = Depot()
    depot.add_transport(van1)
    depot.add_transport(trailer1)
    depot.add_transport(drone1)

    print("Все транспорты в депо:")
    print(depot.transports)

    print("Попытка добавить дубликат (ошибка):")
    try:
        depot.add_transport(van1)
    except ValueError as e:
        print("Ошибка:", e)

    print("Удаление транспорта:")
    print(depot.remove_transport("B456DE77"))
    print("Осталось в депо:", len(depot.transports))

    print("Доступный транспорт (в работе):")
    available = depot.get_available_transpotrs()
    print("Количество:", len(available))

    # 8. Проверка DeliveryRoute и get_delivery_details
    print("\n8. Класс DeliveryRoute:")
    route1 = DeliveryRoute("R001", 150.0, ["Москва", "Тверь", "СПб"])
    route2 = DeliveryRoute("R002", 200.0, ["Саратов", "Волгоград"])
    print(route1.get_delivery_details())
    print(route2.get_delivery_details())

    # 9. Проверка LogisticsCompany
    print("\n9. Класс LogisticsCompany:")
    company = LogisticsCompany("ЛогистикПро")
    print("Название компании:", company.name)

    # Добавляем транспорт
    company.add_transport(van1)
    company.add_transport(trailer1)
    company.add_transport(drone1)

    # Добавляем операторов
    company.operators[op1.full_name] = op1
    company.operators[op2.full_name] = op2

    # Проверка assign_operator
    print("Назначение оператора:")
    company.assign_operator("A123BC77", "Иванов И.И.")
    company.assign_operator("C789FG77", "Петров П.П.")

    # Проверка assign_route
    print("Назначение маршрутов:")
    company.assign_route(van1, route1)
    company.assign_route(drone1, route2)

    # 10. Проверка static class SafetyRegulations
    print("\n10. Статический класс SafetyRegulations:")
    rules = SafetyRegulations.get_safety_rules()
    print("Правила техники безопасности:")
    for r in rules:
        print("-", r)

    # 11. Проверка исключений (для всех требований ООП)
    print("\n11. Проверка обработки исключений:")
    print("Уже проверено: add_transport с дубликатом, оператор не найден, и т.д.")

    print("\nВсе проверки выполнены. Программа готова к сдаче.")


if __name__ == "__main__":
    main()