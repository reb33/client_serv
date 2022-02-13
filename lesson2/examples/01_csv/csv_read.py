""" Module csv_read """

import csv
from pprint import pprint

print('----- Простое чтение из файла kp_data.csv ------')
print('----- Получаем итератор объекта ------')
with open('kp_data.csv', encoding='utf-8') as f_n:
    F_N_READER = csv.reader(f_n)
    print(type(F_N_READER))
    for row in F_N_READER:
        print(row)

print()
print('----- Можно прочитать как обычный текстовой файл ------')
with open('kp_data.csv', encoding='utf-8') as f_n:
    F_N_READER = f_n.read()
    print(type(F_N_READER))
    print(F_N_READER)

print()
print('----- Преобразование итератора в список ------')
with open('kp_data.csv', encoding='utf-8') as f_n:
    F_N_READER = csv.reader(f_n)
    print(type(F_N_READER))
    pprint(list(F_N_READER))


print()
print('----- Разделение строки заголовков от содержимого ------')
with open('kp_data.csv', encoding='utf-8') as f_n:
    F_N_READER = csv.reader(f_n)
    F_N_HEADERS = next(F_N_READER)
    print('Headers: ', F_N_HEADERS)
    for row in F_N_READER:
        print(row)


print()
print('----- Вывод результата с помощью метода DictReader ------')
with open('kp_data.csv', encoding='utf-8') as f_n:
    F_N_READER = csv.DictReader(f_n)
    for row in F_N_READER:
        print(row)
        print(row['hostname'], row['model'])
