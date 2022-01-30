#!/usr/bin/python3
import re

def json_pars(testing_json: str) -> str:
    '''
    json_pars - функция для проверки корректности json-данных, переданных серверу
       задачи:
         1) Установить, что на вход поданы данные в формате json
         2) Установить, что json содержит только одну пару ключ-значение 
         3) Установить, что ключем является строка 'url'
         4) Установить, что в качестве значения передан url, который содержит архив
    '''
    if bool(re.search(r'^{.+?}$', testing_json)):
        pars_json = re.findall(r'"(.+?)"', testing_json)
        if (len(pars_json) == 2) and (pars_json[0].lower() == 'url') and (pars_json[1][-7:].lower() == '.tar.gz'):
            return pars_json[1]

if __name__ == '__main__':
    # тестирование
    json_s = '{"url":"http://127.0.0.1/test.tar.gz"}'
    print(json_pars(json_s))
    print(type(json_pars(json_s)))
