import dis
from typing import Callable


class ClientVerifier(type):

    def __new__(mcs, future_class_name, future_class_parents, future_class_attrs):
        """отсутствие вызовов accept и listen для сокетов;
        использование сокетов для работы по TCP;"""
        methods = []
        for attr in future_class_attrs:
            if isinstance(future_class_attrs[attr], Callable):
                for i in dis.get_instructions(future_class_attrs[attr]):
                    if i.opname in ('LOAD_GLOBAL', 'LOAD_METHOD'):
                        methods.append(i.argval)
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError('В классе обнаружено использование запрещённого метода')
        if 'receive_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')
        return super().__new__(mcs, future_class_name, future_class_parents, future_class_attrs)


class ServerVerifier(type):

    def __new__(mcs, future_class_name, future_class_parents, future_class_attrs):
        """отсутствие вызовов connect для сокетов;
        использование сокетов для работы по TCP."""
        methods = []
        for attr in future_class_attrs:
            if isinstance(future_class_attrs[attr], Callable):
                for i in dis.get_instructions(future_class_attrs[attr]):
                    if i.opname in ('LOAD_GLOBAL', 'LOAD_METHOD'):
                        methods.append(i.argval)
        for command in ('connect',):
            if command in methods:
                raise TypeError('В классе обнаружено использование запрещённого метода')
        if 'receive_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')
        return super().__new__(mcs, future_class_name, future_class_parents, future_class_attrs)
# class A(metaclass=ClientVerifier):
#     x: int
#     y: int
#
#     def __init__(self) -> None:
#         self.q = 5
#         print(123)
#         self.m1()
#         f = math.factorial(5)
#         super().__init__()
#
#     def m1(self):
#         pass
#
#     def m2(self):
#         pass
#
#
# A()