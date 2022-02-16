# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
# Важно: решение должно быть универсальным, т.е. не зависеть от того, какие конкретно слова мы исследуем.
from ast import literal_eval
from contextlib import suppress


def is_converted_to_byte(string):
    with suppress(SyntaxError):
        literal_eval("b'{}'".format(string))
        return True
    return False


def main():
    arr = ['attribute', 'класс', 'функция', 'type']
    for i in arr:
        print(f'{i}  -   {"можно" if is_converted_to_byte(i) else "нельзя"} записать в байтовом типе')


if __name__ == '__main__':
    main()
