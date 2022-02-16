# Задание на закрепление знаний по модулю CSV.
# Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt
# и формирующий новый «отчетный» файл в формате CSV.
#
# Для этого:
# Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
# их открытие и считывание данных.
# В этой функции из считанных данных необходимо
# с помощью регулярных выражений извлечь значения параметров
# «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
# Значения каждого параметра поместить в соответствующий список.
# Должно получиться четыре списка — например,
# os_prod_list, os_name_list, os_code_list, os_type_list.
# В этой же функции создать главный список для хранения данных отчета — например,
# main_data — и поместить в него названия столбцов отчета в виде списка:
# «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
# Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
# Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
# В этой функции реализовать получение данных через вызов функции get_data(),
# а также сохранение подготовленных данных в соответствующий CSV-файл;
# Проверить работу программы через вызов функции write_to_csv().
import csv
import re

import chardet


def get_data(file_names):
    main_data = {'Изготовитель системы': [], 'Название ОС': [], 'Код продукта': [], 'Тип системы': []}
    for file_name in file_names:
        with open(file_name, 'rb') as file:
            file_content = file.read()
            res = chardet.detect(file_content)
            file_content = file_content.decode(encoding=res['encoding'])
            for k, v in main_data.items():
                v.append(re.search(fr'{k}:\s*([^\r\n]+)', file_content).group(1).strip())
    os_prod_list = main_data['Изготовитель системы']
    os_name_list = main_data['Название ОС']
    os_code_list = main_data['Код продукта']
    os_type_list = main_data['Тип системы']
    main_data = list(main_data.keys())
    return main_data, os_prod_list, os_name_list, os_code_list, os_type_list


def write_to_csv(file_names, report_file):
    main_data, os_prod_list, os_name_list, os_code_list, os_type_list = get_data(file_names)
    csv_writer = csv.writer(report_file, quoting=csv.QUOTE_NONNUMERIC)
    csv_writer.writerow(main_data)
    for row in zip(os_prod_list, os_name_list, os_code_list, os_type_list):
        csv_writer.writerow(row)


def main():
    with open('main_data.csv', 'w', encoding='utf-8') as report_file:
        write_to_csv(
            [
                'homework_materials/info_1.txt',
                'homework_materials/info_2.txt',
                'homework_materials/info_3.txt'
            ],
            report_file
        )


if __name__ == '__main__':
    main()
