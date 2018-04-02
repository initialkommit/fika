import traceback
import os
from os import listdir
from os.path import join, isfile, isdir

import errno


def count_files_recursive(input_dir, file_extension=None):
    count = 0
    try:
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

    except:
        traceback.print_exc()
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


if __name__ == '__main__':
    from pathlib import Path
    a = Path(__file__).resolve().parents[0]
    # directory = os.path.join(, "images")
    directory = a / "images"
    print('directory', directory)
