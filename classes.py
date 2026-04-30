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


from abc import ABC, abstractmethod

class Transport(ABC):

    _exicting_transport = set()

    def __new__(cls, gos_number, *args, **kwargs):
        if gos_number in cls._exicting_transport:
            raise ValueError(f"транспорт с номером '{gos_number}' уже существует")
        
        instance = super().__new__(cls)
        cls._exicting_transport.add(gos_number)
        return instance

    def __init__(self, gos_number, brand, capacity):
        if not isinstance(gos_number, str) or not gos_number.strip():
            raise ValueError("Госномер должен быть непустой строкой")
        if not isinstance(brand, str) or not brand.strip():
            raise ValueError("Бренд должен быть непустой строкой")
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Вместимость должна быть положительным числом")
        self._gos_number = gos_number
        self._brand = brand
        self._capacity = capacity
        self._status = "в работе"

    @property
    def gos_number(self):
        return self._gos_number
    
    @property
    def brand(self):
        return self._brand
    
    @property
    def capacity(self):
        return self._capacity
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        if value in ["в работе", "на ремонте"]:
            self._status = value
        else:
            raise ValueError("Недопустимый статус")
    
    @abstractmethod 
    def start_delivery(self):
        pass

    def __str__(self): 
        return f"({self.gos_number}): бренд: {self.brand}, вместимость: {self.capacity}, статус: {self.status}"
    

class Van(Transport):
    def __init__(self, gos_number, brand, capacity, volume, engine_type):
        super().__init__(gos_number, brand, capacity)
        if not isinstance(volume, (int, float)) or volume <= 0:
            raise ValueError("Объем кузова должен быть положительным числом")
        if engine_type not in ["бензин", "электричество"]:
            raise ValueError("Тип двигателя должен быть 'бензин' или 'электричество'")
        self._volume = volume
        self._engine_type = engine_type
    
    @property
    def volume(self):
        return self._volume
    
    @property
    def engine_type(self):
        return self._engine_type
    
    def start_delivery(self):
        return f"Van {self.gos_number} начинает доставку (объем кузова: {self.volume} м^3)"
    

class Trailer(Transport):
    def __init__(self, gos_number, brand, capacity, max_load, trailer_type):
        super().__init__(gos_number, brand, capacity)
        if not isinstance(max_load, (int, float)) or max_load <= 0:
            raise ValueError("Максимальная нагрузка должна быть положительным числом")
        if trailer_type not in ["рефрижератор", "открытый"]:
            raise ValueError("Тип прицепа должен быть 'рефрижератор' или 'открытый'")
        self._max_load = max_load
        self._trailer_type = trailer_type
    
    @property
    def max_load(self):
        return self._max_load
    
    @property
    def trailer_type(self):
        return self._trailer_type
    
    def start_delivery(self):
        return f"Trailer {self.gos_number} начинает доставку (макс нагрузка: {self.max_load}т)"

class Drone(Transport):
    def __init__(self, gos_number, brand, capacity, range_km, payload_kg):
        super().__init__(gos_number, brand, capacity)
        if not isinstance(range_km, (int, float)) or range_km <= 0 or range_km > 1000:
            raise ValueError("Дальность полета должна быть положительным числом до 1000 км")
        if not isinstance(payload_kg, (int, float)) or payload_kg <= 0 or payload_kg > 50:
            raise ValueError("Грузоподъемность должна быть положительным числом до 50 кг")
        self._range_km = range_km
        self._payload_kg = payload_kg
    
    @property
    def range_km(self):
        return self._range_km
    
    @property
    def payload_kg(self):
        return self._payload_kg
    
    def start_delivery(self):
        return f"Drone {self.gos_number} начинает доставку (дальность полёта: {self.range_km}км)"
    

class Maintainable(ABC):
    @abstractmethod
    def perform_maintenance(self):
        pass

class VanMaintainable(Van, Maintainable):
    def perform_maintenance(self):
        if self.engine_type == "электричество":
            if self.status == "на ремонте":
                self.status = "в работе"
                return f"Электрофургон {self.gos_number} обслужен, транспорт в работе"
            else:
                self.status = "на ремонте"
                return f"Электрофургон {self.gos_number} на ремонте"
        else:
            return f"Фургон {self.gos_number} с бензиновым двигателем не требует обслуживания"

class TrailerMaintainable(Trailer, Maintainable):
    def perform_maintenance(self):
        if self.status == "на ремонте":
            self.status = "в работе"
            self._max_load += 1 
            return f"Прицеп {self.gos_number} обслужен, нагрузка увеличена до {self.max_load} т, транспорт в работе"
        else:
            self.status = "на ремонте"
            return f"Прицеп {self.gos_number} на ремонте"

class DroneMaintainable(Drone, Maintainable):
    def perform_maintenance(self):
        if self.payload_kg > 5:
            if self.status == "на ремонте":
                self.status = "в работе"
                return f"Дрон {self.gos_number} обслужен, транспорт в работе"
            else:
                self.status = "на ремонте"
                return f"Дрон {self.gos_number} на ремонте"
        else:
            return f"Дрон {self.gos_number} с низкой грузоподъемностью ({self.payload_kg} кг) не обслуживается"

class Operator:
    def __init__(self, full_name, experience_years, license):
        if not isinstance(full_name, str) or not full_name.strip():
            raise ValueError("ФИО должно быть непустой строкой")
        if not isinstance(experience_years, int) or experience_years < 0:
            raise ValueError("Опыт работы должен быть неотрицательным целым числом")
        if license not in ["грузовой транспорт", "дроны"]:
            raise ValueError("Лицензия должна быть 'грузовой транспорт' или 'дроны'")
        self._full_name = full_name
        self._experience_years = experience_years
        self._license = license
    
    @property
    def full_name(self):
        return self._full_name
    
    @property
    def experience_years(self):
        return self._experience_years
    
    @property
    def license(self):
        return self._license
    
    def operate_vehicle(self, transport):
        return f"Оператор {self.full_name} начинает работу с {transport}"
    
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