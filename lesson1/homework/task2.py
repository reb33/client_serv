# Каждое из слов «class», «function», «method» записать в байтовом типе
# без преобразования в последовательность кодов (не используя методы encode и decode)
# и определить тип, содержимое и длину соответствующих переменных.
from ast import literal_eval


def print_type_value_and_len(bts):
    print(f'{type(bts)}   -   {bts}   -   {len(bts)}')


def convert_to_byte(string):
    return literal_eval("b'{}'".format(string))


def main():
    arr = ['class', 'function', 'method']
    for i in arr:
        print_type_value_and_len(convert_to_byte(i))


if __name__ == '__main__':
    main()
