class IncorrectPort(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__('указан некорректный порт')


class IncorrectResponseFromServer(Exception):
    pass
