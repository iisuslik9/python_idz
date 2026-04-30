from classes import Van, Trailer, Drone
from classes import VanMaintainable, TrailerMaintainable, DroneMaintainable
from classes import Operator, Depot, DeliveryRoute, LogisticsCompany
from classes import SafetyRegulations


def main():


    # 1. Проверка Transport: __new__, __str__, status, дубли
    print("1. Проверка базового класса Transport и дублирования номера:")
    van1 = Van("A123BC77", "Mercedes", 10, 50.0, "бензин")
    trailer1 = Trailer("B456DE77", "Volvo", 20, 25.0, "рефрижератор")
    drone1 = Drone("C789FG77", "DJI", 5, 100.0, 2.0)

    print(van1)
    print(trailer1)
    print(drone1)

    # 1.1 Попытка создать дубликат по номеру 
    print("\nПопытка создать дубликат номера:")
    try:
        van2 = Van("A123BC77", "Ford", 8, 30.0, "электричество")
    except ValueError as e:
        print("Ошибка:", e)

    # 1.2 Проверка статуса через property
    print("\nПроверка статуса (инкапсуляция + property):")
    van1.status = "на ремонте"
    print(van1.status)
    try:
        van1.status = "неизвестный статус"
    except ValueError as e:
        print("Ошибка недопустимого статуса:", e)


    # 2. Полиморфизм через start_delivery
    print("\n2. Полиморфизм через переопределение start_delivery:")
    print(van1.start_delivery())
    print(trailer1.start_delivery())
    print(drone1.start_delivery())


    # 3. Интерфейс Maintainable и полиморфизм
    print("\n3. Проверка интерфейса Maintainable (разные варианты perform_maintenance):")

    van_maint_elec = VanMaintainable("D999ZZ77", "Tesla", 8, 40.0, "электричество")
    van_maint_benz = VanMaintainable("E111EE77", "Ford", 8, 35.0, "бензин")
    trailer_maint = TrailerMaintainable("F222FF77", "Scania", 18, 20.0, "открытый")
    drone_maint = DroneMaintainable("G333GG77", "Parrot", 4, 80.0, 7.0)

    maintainables = [van_maint_elec, van_maint_benz, trailer_maint, drone_maint]

    for m in maintainables:
        print("До ТО:", m, f"[статус={m.status}]")
        print("  perform_maintenance:", m.perform_maintenance())
        print("После:", m, f"[статус={m.status}]\n")


    # 4. Класс Operator и operate_vehicle
    print("4. Класс Operator и operate_vehicle:")
    op1 = Operator("Иванов И.И.", 5, "грузовой транспорт")
    op2 = Operator("Петров П.П.", 3, "дроны")

    print(op1.operate_vehicle(van1))
    print(op2.operate_vehicle(drone1))


    # 5. Класс Depot: добавление, удаление, доступный транспорт
    print("\n5. Класс Depot (хранение транспорта):")
    depot = Depot()
    depot.add_transport(van1)
    depot.add_transport(trailer1)
    depot.add_transport(drone1)

    print("Все транспорты в депо:")
    for t in depot.transports:
        print(" -", t)

    # 5.1 Попытка добавить дубликат
    print("\nПопытка добавить дубликат транспорта:")
    try:
        depot.add_transport(van1)
    except ValueError as e:
        print("Ошибка:", e)

    # 5.2 Удаление транспорта + проверка пустого депо
    print("\nУдаление транспорта:")
    print(depot.remove_transport("B456DE77"))
    print("Осталось в депо:", len(depot.transports))

    # 5.3 Доступный транспорт (в работе)
    print("\nДоступный транспорт (в работе):")
    available = depot.get_available_transports()
    for t in available:
        print(" -", t)


    # 6. Класс DeliveryRoute и get_delivery_details
    print("\n6. Класс DeliveryRoute (property и get_delivery_details):")
    route1 = DeliveryRoute("R001", 150.0, ["Москва", "Тверь", "СПб"])
    route2 = DeliveryRoute("R002", 200.0, ["Саратов", "Волгоград"])

    print(route1.get_delivery_details())
    print(route2.get_delivery_details())


    # 7. Класс LogisticsCompany: управляет Depot, операторами и маршрутами
    print("\n7. Класс LogisticsCompany (управление логистикой):")
    company = LogisticsCompany("ЛогистикПро")
    print("Название компании:", company.name)

    # 7.1 Добавление транспорта через компанию
    company.add_transport(van1)
    company.add_transport(trailer1)
    company.add_transport(drone1)

    # 7.2 Добавление операторов
    company.add_operator(op1)
    company.add_operator(op2)

    # 7.3 Проверка дубликата оператора
    print("Попытка добавить оператора повторно:")
    try:
        company.add_operator(op1)
    except ValueError as e:
        print("Ошибка:", e)

    # 7.4 Назначение операторов на транспорт
    print("\nНазначение операторов:")
    company.assign_operator("A123BC77", "Иванов И.И.")
    company.assign_operator("C789FG77", "Петров П.П.")

    # 7.5 Назначение маршрутов
    print("\nНазначение маршрутов:")
    company.assign_route(van1, route1)
    company.assign_route(drone1, route2)

    # 7.6 Попытка назначить несуществующий оператор
    print("\nПопытка назначить несуществующего оператора:")
    try:
        company.assign_operator("A123BC77", "Неизвестный Оператор")
    except ValueError as e:
        print("Ошибка:", e)

    # 7.7 Удаление оператора
    print("\nУдаление оператора:")
    company.remove_operator("Иванов И.И.")
    print("Осталось операторов:", len(company.operators))
    try:
        company.remove_operator("Несуществующий Оператор")
    except ValueError as e:
        print("Ошибка:", e)


    # 8. Статический класс SafetyRegulations
    print("\n8. Статический класс SafetyRegulations:")
    rules = SafetyRegulations.get_safety_rules()
    print("Правила техники безопасности:")
    for r in rules:
        print(" -", r)




    # 1. Edge‑кейс: дрон с низкой грузоподъёмностью, который не обслуживается
    print("1. Дрон с низкой грузоподъёмностью (не обслуживается):")
    low_payload_drone = DroneMaintainable(
        gos_number="H444HH77",
        brand="TinyDrone",
        capacity=1,
        range_km=10.0,
        payload_kg=2.0    # меньше 5 → не обслуживается
    )
    print("До:", low_payload_drone, f"[грузоподъёмность={low_payload_drone.payload_kg} кг]")
    result = low_payload_drone.perform_maintenance()
    print("→ perform_maintenance:", result)
    print("После:", low_payload_drone, f"[статус={low_payload_drone.status}]")

    # 1.1 вручную установить статус и снова обслужить
    print("\n1.1 Попытка вручную перевести дрон с низкой грузоподъёмностью в любой статус и обслужить:")
    low_payload_drone.status = "на ремонте"   # принудительно ставим
    print("Статус перед обслуживанием:", low_payload_drone.status)
    result = low_payload_drone.perform_maintenance()
    print(" perform_maintenance:", result)
    print("Статус после:", low_payload_drone.status)   # должен остаться "на ремонте"

    # 2. дрон с грузоподъёмностью ровно 5 (граница правила)
    print("\n2. Дрон с грузоподъёмностью ровно 5 кг (граница обслуживания):")
    border_drone = DroneMaintainable(
        gos_number="I555II77",
        brand="BorderDrone",
        capacity=4,
        range_km=60.0,
        payload_kg=5.0   
    )
    print("До:", border_drone, f"[грузоподъёмность={border_drone.payload_kg} кг]")
    result = border_drone.perform_maintenance()
    print("→ perform_maintenance:", result)
    print("После:", border_drone, f"[статус={border_drone.status}]")

    # 3. дрон с payload  0 (теоретический минимум)
    print("\n3. Дрон с грузоподъёмностью 0 кг (min edge):")
    try:
        zero_payload_drone = DroneMaintainable(
            gos_number="J000JJ77",
            brand="ZeroPayload",
            capacity=3,
            range_km=50.0,
            payload_kg=0.0
        )
        print("До:", zero_payload_drone, f"[грузоподъёмность={zero_payload_drone.payload_kg} кг]")
        result = zero_payload_drone.perform_maintenance()
        print(" perform_maintenance:", result)
        print("После:", zero_payload_drone, f"[статус={zero_payload_drone.status}]")
    except ValueError as e:
        print("Ошибка при создании дрона с payload=0:", e)

    # 4.  дрон переведён в 
    print("\n4. Попытка обслужить дрон с неизвестным статусом:")
    valid_drone = DroneMaintainable(
        gos_number="K111KK77",
        brand="TestDrone",
        capacity=4,
        range_km=100.0,
        payload_kg=10.0   # обслуживается
    )
    print("До корректного статуса:", valid_drone.status)
    # вручную устанавливаем недопустимый статус (через setter)
    try:
        valid_drone.status = "тестовый статус"
    except ValueError as e:
        print("Ошибка при установке недопустимого статуса:", e)

    # корректно устанавливаем статус "на ремонте"
    valid_drone.status = "на ремонте"
    print("После установки корректного статуса:", valid_drone.status)
    result = valid_drone.perform_maintenance()
    print("  perform_maintenance:", result)
    print("Конечный статус:", valid_drone.status)

    # 5. попытка обслужить ван без электричество/бензин двигателя
    print("\n5. Ван с нестандартным типом двигателя (не 'электричество' и не 'бензин'):")
    try:
        weird_van = VanMaintainable(
            gos_number="L999LL77",
            brand="WeirdVan",
            capacity=12,
            volume=45.0,
            engine_type="водород"   
        )
        print("До:", weird_van, f"[двигатель={weird_van.engine_type}]")
        result = weird_van.perform_maintenance()
        print(" perform_maintenance:", result)   # не требует обслуживания
        print("После:", weird_van, f"[статус={weird_van.status}]")
    except ValueError as e:
        print("Ошибка при создании вана с нестандартным двигателем:", e)

    # 6. van в статусе невалидный (через setter)
    print("\n6. van с неизвестным статусом (через setter):")
    test_van = VanMaintainable(
        gos_number="M111MM77",
        brand="TestVan",
        capacity=10,
        volume=50.0,
        engine_type="электричество"
    )
    print("Исходный статус:", test_van.status)
    try:
        test_van.status = "невалидный статус"
    except ValueError as e:
        print("Ошибка при установке недопустимого статуса:", e)

    # устанавливаем валидный статус для обслуживания
    test_van.status = "на ремонте"
    print("После валидного статуса:", test_van.status)
    result = test_van.perform_maintenance()
    print("  perform_maintenance:", result)
    print("Конечный статус:", test_van.status)

    # 7. прицеп с максимальной нагрузкой 0 или 1 т
    print("\n7. Прицеп с граничной нагрузкой (0 и 1 т):")
    try:
        trailer_zero = TrailerMaintainable(
            gos_number="N000NN77",
            brand="ZeroLoad",
            capacity=15,
            max_load=0.0,
            trailer_type="открытый"
        )
        print(f"До: {trailer_zero} (макс нагрузка {trailer_zero.max_load} т)")
        trailer_zero.status = "на ремонте"
        result = trailer_zero.perform_maintenance()
        print(" perform_maintenance:", result)
        print(f"После: {trailer_zero} (макс нагрузка {trailer_zero.max_load} т, статус {trailer_zero.status})\n")
    except ValueError as e:
        print("Ошибка при создании прицепа с max_load=0:", e)

    trailer_one = TrailerMaintainable(
        gos_number="N111NN77",
        brand="OneTonne",
        capacity=16,
        max_load=1.0,
        trailer_type="рефрижератор"
    )
    print(f"До: {trailer_one} (макс нагрузка {trailer_one.max_load} т)")
    trailer_one.status = "на ремонте"
    result = trailer_one.perform_maintenance()
    print(" perform_maintenance:", result)
    print(f"После: {trailer_one} (макс нагрузка {trailer_one.max_load} т, статус {trailer_one.status})\n")


if __name__ == "__main__":
    main()