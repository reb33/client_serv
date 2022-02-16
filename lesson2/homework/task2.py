# 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
# Написать скрипт, автоматизирующий его заполнение данными. Для этого:
# Создать функцию write_order_to_json(), в которую передается 5 параметров —
# товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date).
# Функция должна предусматривать запись данных в виде словаря в файл orders.json.
# При записи данных указать величину отступа в 4 пробельных символа;
# Проверить работу программы через вызов функции write_order_to_json()
# с передачей в нее значений каждого параметра.
import json
from datetime import datetime


def write_order_to_json(item, quantity, price, buyer, date):
    with open('homework_materials/orders.json', encoding='utf-8') as file:
        orders = json.load(file)['orders']
    orders.append({
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    })
    with open('homework_materials/orders.json', 'w', encoding='utf-8') as file:
        json.dump({'orders': orders}, file, indent=4, default=str)


def main():
    for i in range(5):
        write_order_to_json(f'item_{i}', quantity=i, price=100+i, buyer=f'buyer_{i}', date=datetime.now())


if __name__ == '__main__':
    main()