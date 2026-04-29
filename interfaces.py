from classes import Van, Trailer, Drone

class Maintainable:
    def perform_maintenance(self):
        if self.status == "на ремонте":
            self.status = "в работе"
            return "ремонт завершен, транспорт в работе"
        else:
            self.status = "на ремонте"
            return "транспорт на ремонте"

class VanMaintainable(Van, Maintainable):
    pass

class TrailerMaintainable(Trailer, Maintainable):
    pass

class DroneMaintainable(Drone, Maintainable):
    pass