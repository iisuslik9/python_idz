from abc import ABC, abstractmethod
from interface import Maintainable

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
    

class Van(Transport, Maintainable):
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

class Trailer(Transport, Maintainable):
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
    
    def perform_maintenance(self):
        if self.status == "на ремонте":
            self.status = "в работе"
            self._max_load += 1 
            return f"Прицеп {self.gos_number} обслужен, нагрузка увеличена до {self.max_load} т, транспорт в работе"
        else:
            self.status = "на ремонте"
            return f"Прицеп {self.gos_number} на ремонте"

class Drone(Transport, Maintainable):
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