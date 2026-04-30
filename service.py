# 1. В созданных классах не должно быть операторов ввода, кроме случаев,
# когда это явно указано в программе. Все данные для проверки работы
# методов классов должны быть описаны в коде.
# 2. Если в задании не указано сколько и какие данные для проверки
# работоспособности функций нужно написать, то вы должны сами их
# придумать и описать в коде.
# 3. Для каждого атрибута всех классов, реализованных в работе,
# необходимо реализовать property – специальные методы для доступа к
# атрибутам.
# 4. В задании необходимо использовать все перечисленные принципы
# ООП: инкапсуляция (защищенные атрибуты, property); наследование,
# полиморфизм: через методы и через интерфейсы; магические методы
# (__str__, __new__ для ограничения дубликатов); использовать обработку
# исключений; использовать статические методы.

# Вариант 4: Система управления логистической компанией
# Разработать систему классов для управления логистическими процессами
# транспортной компании.
# 1. Базовый класс Transport (Абстрактный)
#  Наследуется от ABC.
#  Атрибуты: Государственный номер, бренд, вместимость, статус
# (например, "в работе", "на ремонте").
#  Свойства (property) для доступа к атрибутам.
#  Абстрактный метод Начало доставки.
#  Магический метод __str__() для вывода информации о транспорте.
#  Метапрограммирование: через __new__ запретить создание транспорта
# с одинаковым Государственным номером.
# 2. Подклассы (Van, Trailer, Drone)
#  Переопределяют start_delivery().
#  Уникальные атрибуты и методы:
# o Van — объем кузова (в кубометрах), тип двигателя
# (бензин/электричество).
# o Trailer — максимальная нагрузка (в тоннах), тип прицепа
# (рефрижератор/открытый).
# o Drone — дальность полета (в км), грузоподъемность (в кг).

# 3. Интерфейс Maintainable
#  Наследуют классы из пункта 2.
#  Обязывает реализовать метод perform_maintenance(), который меняет
# статус транспорта на "на ремонте" и обратно.
# 4. Класс Operator
#  Атрибуты: ФИО, опыт работы (в годах), лицензия (например,
# "грузовой транспорт", "дроны").
#  Свойства: для доступа к атрибутам.
#  Метод operate_vehicle(), принимающий объект Transport и выводящий
# сообщение о начале работы с транспортом.
# 5. Класс Depot (Склад)
#  Хранит список всех транспортных средств.
#  Методы: добавление транспорта (с обработкой исключений при
# дублировании); удаление транспорта; возврат списка транспорта со
# статусом "в работе".
# 6. Класс DeliveryRoute (Маршрут доставки)
#  Атрибуты: идентификатор маршрута, расстояние (в км), список точек
# доставки.
#  Свойства: для доступа к атрибутам.
#  Метод get_delivery_details() — возвращает информацию о маршруте.
# 7. Класс LogisticsCompany (Логистическая компания)
#  Управляет складом (Depot).
#  Назначает маршруты (DeliveryRoute) транспортным средствам.
#  Метод assign_operator() — назначает оператора на транспорт.
# 8. Статический класс SafetyRegulations
#  Статический метод get_safety_rules() — возвращает правила техники
# безопасности для эксплуатации транспорта.

from model import Operator

class Depot:
    def __init__(self):
        self._transports = []

    @property
    def transports(self):
        return self._transports.copy()

    def add_transport(self, transport):
        if transport.gos_number in [t.gos_number for t in self._transports]:
            raise ValueError(f"транспорт {transport.gos_number} уже добавлен")
        self._transports.append(transport)

    def remove_transport(self, gos_number):
        if not self._transports:
            raise ValueError(f"депо пустое, транспорт с номером {gos_number} не найден")
        for t in self._transports:
            if t.gos_number == gos_number:
                self._transports.remove(t)
                return f"транспорт {gos_number} удален"
        raise ValueError(f"транспорт с номером {gos_number} не найден")
        

    def get_available_transports(self):
        return [t for t in self.transports if t.status == "в работе"]
    
class DeliveryRoute():
    def __init__(self, route_id, distance_km, delivery_points):
        if not isinstance(route_id, str) or not route_id.strip():
            raise ValueError("Идентификатор маршрута должен быть непустой строкой")
        if not isinstance(distance_km, (int, float)) or distance_km <= 0:
            raise ValueError("Расстояние должно быть положительным числом")
        if not isinstance(delivery_points, list) or not delivery_points or not all(isinstance(p, str) and p.strip() for p in delivery_points):
            raise ValueError("Точки доставки должны быть непустым списком непустых строк")
        self._route_id = route_id
        self._distance_km = distance_km
        self._delivery_points = delivery_points
    
    @property
    def route_id(self):
        return self._route_id

    @property
    def distance_km(self):
        return self._distance_km

    @property
    def delivery_points(self):
        return self._delivery_points.copy()

    def get_delivery_details(self):
        points = ", ".join(self.delivery_points)
        return f"маршрут {self.route_id}: {self.distance_km}км, точки: {points}"


class LogisticsCompany:
    def __init__(self, name):
        self.name = name
        self.depot = Depot()
        self.operators = {}
        self.assignments = {}
    
    def add_transport(self, transport):
        self.depot.add_transport(transport)

    
    def add_operator(self, operator: Operator):
        if operator.full_name in self.operators:
            raise ValueError(f"Оператор {operator.full_name} уже существует")
        self.operators[operator.full_name] = operator

    def remove_operator(self, operator_name: str):
        if operator_name not in self.operators:
            raise ValueError(f"Оператор {operator_name} не найден")
        del self.operators[operator_name]
    
    def assign_route(self, transport, route):
        print(f"{transport.start_delivery()} по маршруту {route.route_id}")
    
    def assign_operator(self, gos_number, operator_name):
        if operator_name not in self.operators:
            raise ValueError(f"оператор {operator_name} не найден")

        self.assignments[gos_number] = operator_name
        op = self.operators[operator_name]
        transport_obj = None
        for t in self.depot.transports:
            if t.gos_number == gos_number:
                transport_obj = t
                break

        if transport_obj:
            print(op.operate_vehicle(transport_obj))

class SafetyRegulations:
    @staticmethod
    def get_safety_rules():
        return [
            "Проверять техническое состояние перед выездом",
            "Не превышать грузоподъемность",
            "Соблюдать скоростной режим"
        ]