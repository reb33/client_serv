"""Модуль pyyaml_examples"""

import yaml  # pip3 install pyyaml

# считываем данные
with open('data_read.yaml', encoding='utf-8') as f_n:
    F_N_CONTENT = yaml.load(f_n, Loader=yaml.FullLoader)
    print(F_N_CONTENT)

# изменяем формат записи (+ для символов юникода)
ACTION_LIST = ['msg_1', 'msg_2', 'msg_3']
TO_LIST = ['Иванов', 'Петров', 'Сидоров']
AS_SET = {1, 2, 3}
DATA_TO_YAML = {'action': ACTION_LIST, 'names': AS_SET, 'to': TO_LIST}

with open('data_write_3.yaml', 'w', encoding='utf-8') as f_n:
    yaml.dump(DATA_TO_YAML, f_n, default_flow_style=False)
    # yaml.dump(DATA_TO_YAML, f_n, default_flow_style=False, allow_unicode=True)

with open('data_write_3.yaml', encoding='utf-8') as f_n:
    F_N_CONTENT = yaml.load(f_n, Loader=yaml.FullLoader)
    print(F_N_CONTENT)


