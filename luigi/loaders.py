import re

import luigi
from luigi.contrib.postgres import CopyToTable

from config.settings import DATABASES
from core.const import ESACPE_CHAR_FOR_NEWLINE
from core.luigi.targets import DBTarget
from core.utils.postgres import get_db_info


class CopyToDB(CopyToTable):
    """선행 태스크 결과물을 DB에 복사해 넣는 클래스"""
    to_database = luigi.ChoiceParameter(choices=['analytics', 'jpercent'],
                                        default='analytics')
    host = None
    database = None
    user = None
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db = get_db_info(DATABASES[self.to_database])
        self.host = db['host']
        self.database = db['database']
        self.user = db['user']
        self.password = db['password']

    def rows(self):
        input_files = self.input()
        if not isinstance(self.input(), list):
            input_files = [self.input()]

        for input_file in input_files:
            with input_file.open('r') as fobj:
                for line in fobj:
                    values = line.strip('\n').split('\t')

                    # 개행문자(\n) 대신 저장했던 문자가 있다면 다시 개행문자로 바꿔준다.
                    for idx, value in enumerate(values):
                        match = re.search('^{}'.format(ESACPE_CHAR_FOR_NEWLINE), value)
                        if match:
                            values[idx] = '\n{}'.format(value[1:])
                    yield values

    def output(self):
        return DBTarget(self.table, self.task_id, to_database=self.to_database)
