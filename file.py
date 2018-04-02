import os.path
import codecs

import chardet
import subprocess

from num import to_readable


class FileUtil(object):
    def __init__(self, data=None):
        self.data = data

    def __repr__(self):
        return self.data

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
        except:
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
        d = os.path.dirname(file_path)
        if len(d) > 0 and not os.path.exists(d):
            os.makedirs(d)
        if is_binary:
            write_mode = 'wb'
            if data and len(data) > 0:
                with open(file_path, mode=write_mode) as f:
                    f.write(data)
        else:  # text data
            write_mode = 'w'
            if data and len(data) > 0:
                with codecs.open(file_path, mode=write_mode, encoding=encoding) as f:
                    f.write(data)

    @staticmethod
    def count_lines(fname):
        p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        result, err = p.communicate()
        if p.returncode != 0:
            raise IOError(err)
        return int(result.strip().split()[0])

    @staticmethod
    def print_n_write(file, s):
        print(s)
        file.write('%s\n' % (s,))

    @staticmethod
    def to_filename(s):
        return s.replace('/', '').replace('"', "'")

    @staticmethod
    def to_filename_from_dict(di, delimeter='_', include=None):
        if include is None:
            include = di.keys()
        return delimeter.join(['{}{}'.format(key.replace(delimeter, ''), to_readable(val)) for key, val in sorted(di.items()) if key in include])


if __name__ == '__main__':
    with open('output/file_test.txt', 'w') as file:
        FileUtil.print_n_write(file, 'aaa')
        FileUtil.print_n_write(file, ('a', 'b', 'c'))
