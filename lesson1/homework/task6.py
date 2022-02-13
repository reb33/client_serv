# Создать текстовый файл test_file.txt,
# заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
# Далее забыть о том, что мы сами только что создали этот файл и исходить из того,
# что перед нами файл в неизвестной кодировке.
# Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.
import chardet


def write_file(file_name, content_lines):
    with open(file_name, 'w') as file:
        file.write("\n".join(content_lines))


def open_file(file_name):
    with open(file_name, 'rb') as file:
        for line in file:
            result = chardet.detect(line)
            print(line.decode(encoding=result['encoding']))


def main():
    arr = ['сетевое программирование', 'сокет', 'декоратор']
    write_file('test_file.txt', arr)
    open_file('test_file.txt')


if __name__ == '__main__':
    main()
