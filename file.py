import os
import codecs

import chardet


class FileUtil:
    """File-related Helper"""
    def __init__(self, data=None):
        self.data = data

    def read(self, file_path, is_binary=False):
        self.data = FileUtil.reads(file_path, is_binary)
        return self.data

    def write(self, file_path, is_binary=False):
        FileUtil.writes(self.data, file_path, is_binary)

    @staticmethod
    def delete(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def encoding(file_path):
        try:
            return chardet.detect(open(file_path).read())['encoding']
        except Exception:
            return None

    @staticmethod
    def reads(file_path, is_binary=False):
        if is_binary:
            read_mode = 'rb'
            with open(file_path, mode=read_mode) as f:
                data = ''.join([line for line in f.readlines()])
            return data
        else:  # text data
            read_mode = 'r'
            charset = FileUtil.encoding(file_path)
            with codecs.open(file_path, mode=read_mode, encoding=charset) as f:
                data = ''.join([line for line in f.readlines()])
            return data

    @staticmethod
    def writes(data, file_path, is_binary=False, encoding='UTF-8'):
        directory = os.path.dirname(file_path)
        if len(directory) > 0 and not os.path.exists(directory):
            os.makedirs(directory)

        if is_binary:
            write_mode = 'wb'
            if data:
                with open(file_path, mode=write_mode) as f:
                    f.write(data)
        else:  # text data
            write_mode = 'w'
            if data:
                with codecs.open(file_path, mode=write_mode, encoding=encoding) as f:
                    f.write(data)
