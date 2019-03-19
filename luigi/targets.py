import os
import tempfile

from luigi.contrib.postgres import PostgresTarget

from config.settings import DATABASES
from core.utils.os import is_local
from core.utils.postgres import get_db_info


def get_localtarget_path(target_dir, filename):
    """Luigi에서 LocalTarget으로 저장할 경로를 Local or Server path를 만들어서 번환한다.

    Args:
        target_dir (str): 저장할 디렉토리 이름
        filename (str): 저장할 파일 이름(확장자 포함)

    Returns:
        (str) path/filename.ext which is different according to OS
    """
    if is_local():
        base_path = tempfile.gettempdir()
    else:
        base_path = '/home/ubuntu/files'

    target_path = '{}/{}'.format(base_path, target_dir)
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    localtarget_path = '{target_path}/{filename}'

    return localtarget_path.format(target_path=target_path, filename=filename)


class DBTarget(PostgresTarget):
    """Target To analytics DB"""
    use_db_timestamps = False  # local datetime, not UTC

    def __init__(self, table, update_id, to_database='analytics'):
        db = get_db_info(DATABASES[to_database])
        super().__init__(db['host'], db['database'], db['user'], db['password'], table, update_id)
