#база данных отлавливает системные ошибки (IntegrityError), 
#переводит их в бизнес-исключения
#интерфейс выводит их пользователю

class DuplicateEntityError(Exception):
    pass

class EntityNotFoundError(Exception):
    pass


VALID_STATUSES = ["на складе", "в пути", "доставлен"]
class InvalidStatusError(Exception):
    pass