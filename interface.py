from abc import ABC, abstractmethod

class Maintainable(ABC):
    @abstractmethod
    def perform_maintenance(self):
        pass

# class VanMaintainable(Van, Maintainable):
#     def perform_maintenance(self):
#         if self.engine_type == "электричество":
#             if self.status == "на ремонте":
#                 self.status = "в работе"
#                 return f"Электрофургон {self.gos_number} обслужен, транспорт в работе"
#             else:
#                 self.status = "на ремонте"
#                 return f"Электрофургон {self.gos_number} на ремонте"
#         else:
#             return f"Фургон {self.gos_number} с бензиновым двигателем не требует обслуживания"

# class TrailerMaintainable(Trailer, Maintainable):
#     def perform_maintenance(self):
#         if self.status == "на ремонте":
#             self.status = "в работе"
#             self._max_load += 1 
#             return f"Прицеп {self.gos_number} обслужен, нагрузка увеличена до {self.max_load} т, транспорт в работе"
#         else:
#             self.status = "на ремонте"
#             return f"Прицеп {self.gos_number} на ремонте"

# class DroneMaintainable(Drone, Maintainable):
#     def perform_maintenance(self):
#         if self.payload_kg > 5:
#             if self.status == "на ремонте":
#                 self.status = "в работе"
#                 return f"Дрон {self.gos_number} обслужен, транспорт в работе"
#             else:
#                 self.status = "на ремонте"
#                 return f"Дрон {self.gos_number} на ремонте"
#         else:
#             return f"Дрон {self.gos_number} с низкой грузоподъемностью ({self.payload_kg} кг) не обслуживается"