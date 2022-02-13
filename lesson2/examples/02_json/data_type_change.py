"""Модуль data_type_change"""

import json
# изменение типа данных при преобразованиях из python в json

TUPLE_EX = (
    "action",
    "to",
    "from",
    "encoding",
    "message"
    )

print(type(TUPLE_EX))

with open('tuple_ex.json', 'w') as f_n:
    json.dump(TUPLE_EX, f_n)

with open('tuple_ex.json') as f_n:
    OBJ = json.load(f_n)
print(type(OBJ))

# ошибка - ограничения по типам данных
DICT_TO_JSON = {('action', 'to'): 'msg', 'from': 'account_name'}

with open('dict_to_json.json', 'w') as f_n:
    json.dump(DICT_TO_JSON, f_n)

# игнорирование ограничения по типам
with open('dict_to_json.json', 'w') as f_n:
    json.dump(DICT_TO_JSON, f_n, skipkeys=True)

with open('dict_to_json.json') as f_n:
    F_N_CONTENT = f_n.read()
    OBJ = json.loads(F_N_CONTENT)
    print(OBJ)

"""
тип данных set в json совершенно не допустим!!!
"""
# DICT_TO_JSON = {('action', 'to'): 'msg', 'from': 'account_name', 'set': {1, 2, 3}}
#
# with open('dict_to_json.json', 'w') as f_n:
#     json.dump(DICT_TO_JSON, f_n, skipkeys=True)


# конвертация ключей-чисел в строку
MY_DICT = {5: 300, 1: 400}
DICT_TO_JSON = json.dumps(MY_DICT)
print(DICT_TO_JSON)
