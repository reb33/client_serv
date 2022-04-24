class IncorrectPort(Exception):
    def __str__(self):
        return 'указан некорректный порт'


class IncorrectDataRecivedError(Exception):
    def __str__(self):
        return 'Принято некорректное сообщение от удалённого компьютера.'


# Исключение - ошибка сервера
class ServerError(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


# Ошибка - отсутствует обязательное поле в принятом словаре.
class ReqFieldMissingError(Exception):
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'В принятом словаре отсутствует обязательное поле {self.missing_field}.'
