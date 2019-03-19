import os
from os import listdir
from os.path import isdir
from os.path import isfile
from os.path import join
import traceback

import errno


def count_files(input_dir, file_extension=None):
    """File의 수를 세서 반환한다.

    Parameters:
        input_dir (str): Path to count files in
        file_extension (str): Certain extension of files to count

    Return:
        count (int): input_dir 에 있는 파일 수
    """
    count = 0
    print('input_dir: ' + input_dir)
    for filename in listdir(input_dir):
        input_path = join(input_dir, filename)

        if isdir(input_path):
            print('%s:%s' % (input_path, count_files_recursive(input_path)))
            count += count_files_recursive(input_path)
        if isfile(input_path):
            if file_extension:
                if filename.endswith(file_extension):
                    count += 1
                    print(input_path)
            else:
                count += 1
    return count


def require_dirs(path):
    """directory 생성"""
    original_mask = os.umask(0)
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
    finally:
        os.umask(original_mask)
