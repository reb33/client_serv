"""
Модуль pyyaml_examples

Attention!!! Need to install!

pip install pyyaml
"""


import yaml

# считываем данные
with open('data_read.yaml', encoding='utf-8') as f_n:
    F_N_CONTENT = yaml.load(f_n, Loader=yaml.FullLoader)
    print(type(F_N_CONTENT))
    print(F_N_CONTENT)

# изменяем формат записи
ACTION_LIST = ['msg_1', 'msg_2', 'msg_3']
TO_LIST = ['account_1', 'account_2', 'account_3']
AS_SET = {1, 2, 2, 3}
DATA_TO_YAML = {'action': ACTION_LIST, 'to': TO_LIST, 'names': AS_SET}

with open('data_write.yaml', 'w', encoding='utf-8') as f_n:
    yaml.dump(DATA_TO_YAML, f_n, default_flow_style=True)

with open('data_write.yaml', encoding='utf-8') as f_n:
    F_N_CONTENT = yaml.load(f_n, Loader=yaml.FullLoader)
    print('type(F_N_CONTENT)', type(F_N_CONTENT))
    print(F_N_CONTENT)

"""
По умолчанию ключи в yaml сортируются
yaml.dump(DATA_TO_YAML, f_n, sort_keys=True)

Это можно отключить с помощью опции sortkeys=False
yaml.dump(DATA_TO_YAML, f_n, sort_keys=False)
"""

with open('data_write_1.yaml', 'w', encoding='utf-8') as f_n:
    yaml.dump(DATA_TO_YAML, f_n, default_flow_style=False, sort_keys=False)

with open('data_write_1.yaml', encoding='utf-8') as f_n:
    F_N_CONTENT = yaml.load(f_n, Loader=yaml.FullLoader)
    print(F_N_CONTENT)

"""
Отступы менять можно с помощью параметра indent (по умолчанию indent=2)
https://pyyaml.org/wiki/PyYAMLDocumentation
"""

with open('data_write_2.yaml', 'w', encoding='utf-8') as f_n:
    yaml.dump(DATA_TO_YAML, f_n, default_flow_style=False, sort_keys=False, indent=4)

with open('data_write_2.yaml', encoding='utf-8') as f_n:
    F_N_CONTENT = yaml.load(f_n, Loader=yaml.FullLoader)
    print(F_N_CONTENT)
