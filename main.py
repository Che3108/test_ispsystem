#!/usr/bin/python3

import socketserver
from my_server import MyHTTPHandler

def start_server(port: int) -> None:
    '''
    start_server - функция для запуска сервера
    '''
    
    # создаем обработчик запросов
    handler = MyHTTPHandler()
    
    # создаем сервер
    server = socketserver.TCPServer(('', port), handler)
    
    # Выводим сообщение о старте сервера
    print(f'Server start at port: {port}')
    
    # стартуем сервер
    server.serve_forever()

if __name__ == '__main__':
    PORT = 8008
    start_server(PORT)
