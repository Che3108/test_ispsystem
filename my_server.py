#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler
import threading
import time
from json_pars import json_pars
from download import DownloadMaster

class MyHTTPHandler(BaseHTTPRequestHandler):
    '''
    MyHTTPHandler - класс для обработки запросов на http-сервер
    '''
    def __init__(self):
        # arh_id_base - словарь для хранения id в качестве ключа и экзепляра класса DownloadMaster
        self.arh_id_base = dict()
        
    def __call__(self, *args, **kwargs):
        # При вызове объекта, запустится инициализация родителя
        super().__init__(*args, **kwargs)

    def do_POST(self):
        # ручка для запуска скачивания архива
        if self.path == '/arhive':
            
            # Достаем информацию из запроса
            content_len = int(self.headers.get('Content-Length'))
            post = self.rfile.read(content_len)
            
            # Проверяем правильность полученной информации с помощью json_pars
            arh_url = json_pars(post.decode('utf-8'))
            
            # если запрос содержит верные входные данные
            if arh_url:
                # то присваиваем id (id - это текущее время в секундах) 
                arh_id = str(int(time.time()))
                
                # записываем в словарь id и обработчик контента
                self.arh_id_base[arh_id] = DownloadMaster(arh_id)
                
                # запускаем загрузку и распаковку архива в отдельном потоке
                th = threading.Thread(
                    target = self.arh_id_base[arh_id].download, 
                    args = (arh_url,)
                )
                th.start()
                
                # отвечаем на запрос, посылая id архива
                answer_code = 200
                answer_mess = '{"id": "'+arh_id+'"}'
            else:
                # иначе посылаем код ошибки и детальную информацию
                answer_code = 406
                answer_mess = '{"detal": "wrong_request"}'
                
            # упаковываем все в ответ и отправляем
            answer_mess = answer_mess.encode('utf-8')
            self.send_response(answer_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(answer_mess)))
            self.end_headers()
            self.wfile.write(answer_mess)

    def do_GET(self):
        # ручка для получения текущего состояния архива
        if self.path == '/arhive':
            # Достаем информацию из запроса
            content_len = int(self.headers.get('Content-Length'))
            get = self.rfile.read(content_len).decode('utf-8')
            
            # Проверяем, что полученная инфомация соответсвует ключу одного из архивов
            if get in self.arh_id_base.keys():
                # если соответствует, то запрашиваем статус и готовим ответ
                answer_code = 200
                answer_mess = self.arh_id_base[get].get_status()
            else:
                # иначе посылаем код ошибки и детальную информацию
                answer_code = 406
                answer_mess = '{"detal": "wrong_id"}'
                
             # упаковываем все в ответ и отправляем
            answer_mess = answer_mess.encode('utf-8')
            self.send_response(answer_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(answer_mess)))
            self.end_headers()
            self.wfile.write(answer_mess)
    
    def do_DELETE(self):
        # ручка для удаления скачанного архива по уникальному идентификатору
        if self.path == '/arhive':
            # Достаем информацию из запроса
            content_len = int(self.headers.get('Content-Length'))
            del_id = self.rfile.read(content_len).decode('utf-8')
            
            # Проверяем, что полученная инфомация соответсвует ключу одного из архивов
            if del_id in self.arh_id_base.keys():
                
                # В отдельном потоке запускаем удаление архива и,
                #     в этом же потоке, удаление информации об архиве из словаря
                th = threading.Thread(
                    target = lambda: [
                        self.arh_id_base[del_id].delete_arh(), 
                        self.arh_id_base.pop(del_id)
                    ]
                )
                th.start()
                
                # готовим ответ
                answer_code = 200
                answer_mess = '{"id": "'+del_id+'", "status": "deleting"}'
            else:
                # иначе посылаем код ошибки и детальную информацию
                answer_code = 406
                answer_mess = '{"detal": "wrong_id"}'
                
             # упаковываем все в ответ и отправляем
            answer_mess = answer_mess.encode('utf-8')
            self.send_response(answer_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(answer_mess)))
            self.end_headers()
            self.wfile.write(answer_mess)