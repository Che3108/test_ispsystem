#!/usr/bin/python3
import re

def json_pars(s: str) -> str:
    '''
    json_pars - функция для проверки корректности json-данных, переданных серверу
       задачи:
         1) Установить, что на вход поданы данные в формате json
         2) Установить, что json содержит только одну пару ключ-значение 
         3) Установить, что ключем является строка 'url'
         4) Установить, что в качестве значения передан url, который содержит архив
    '''
    if bool(re.search(r'^{.+?}$', s)):
        jn = re.findall(r'"(.+?)"', s)
        if (len(jn) == 2) and (jn[0].lower() == 'url') and (jn[1][-7:].lower() == '.tar.gz'):
            return jn[1]

if __name__ == '__main__':
    # тестирование
    s = '{"url":"http://127.0.0.1/test.tar.gz"}'
    print(json_pars(s))
    print(type(json_pars(s)))
