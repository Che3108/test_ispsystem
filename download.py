#!/usr/bin/python3

import tarfile
import json
import os
import shutil
import requests
from requests.exceptions import HTTPError

class DownloadMaster(object):
    '''
    DownloadMaster - класс для управления контентом (загрузка, распаковка, удаление, состояние)
        При инициализации объекта необходимо подать уникальный его уникитальный номер в виде строки
    '''
    def __init__(self, id_arh: str, chunk_size = 1024) -> None:
        self.chunk_size = chunk_size
        self.id = id_arh
        self.status_list = ['downloading', 'unpacking', 'ok', 'deleting', 'unknown']
        self.status = self.status_list[-1]

    def download(self, url: str):
        """
        download - функция загрузки архива
            На вход получает url-адрес и загружает архив
            При неудаче в знании статуса возращает строку с ошибкой
        """
        self.url = url
        self.file_name = self.id+'.tar.gz'
        self.download_pe_cent = 0
        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()
            if response.status_code == 200:
                if response.headers['Content-Type'] == 'application/octet-stream':
                    Content_Length = int(response.headers['Content-Length'])
                    with open(self.file_name, 'wb') as f:
                        for i, chunk in enumerate(response.iter_content(chunk_size=self.chunk_size)):
                            if chunk:
                                f.write(chunk)
                                self.status = self.status_list[0]
                                self.download_pe_cent = int(i*self.chunk_size / Content_Length *100)
        except HTTPError as http_err:
            self.status = f'HTTP error occurred: {http_err}'
        except Exception as err:
            self.status = f'Other error occurred: {err}'
        else:
            self.extract()
            self.status = self.status_list[2]

    def extract(self) -> None:
        '''
        extract - функция извлечения данных из архива
        '''
        with tarfile.open(self.file_name) as tar:
            self.status = self.status_list[1]
            self.files = tar.getnames()
            tar.extractall(path=self.id)

    def delete_arh(self) -> None:
        '''
        delete_arh - функция удаления архива и распакованных файлов
        '''
        self.status = self.status_list[3]
        os.remove(os.path.join(os.getcwd(), self.file_name))
        arh_unpack_dir = os.path.join(os.getcwd(), self.id)
        shutil.rmtree(arh_unpack_dir)

    def get_status(self) -> str:
        '''
        get_status - функция получения текущего состояния контента
        '''
        status = {'id':self.id}
        if self.status == self.status_list[0]:
            status['status'] = self.status
            status['progress'] = self.download_pe_cent
        elif self.status == self.status_list[2]:
            status['status'] = self.status
            status['files'] = self.files
        else:
            status['status'] = self.status
        return json.dumps(status)


if __name__ == '__main__':
    # Тестирование работы
    url ='http://download.ispsystem.com/OSTemplate/new/latest/Debian-7-i386-5.57-20170910000.tar.gz'
    dm = DownloadMaster('20170910000')
    dm.download(url)
    dm.delete_arh()
