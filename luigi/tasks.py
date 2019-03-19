import numpy as np
from contextlib import closing

import luigi
import pandas as pd
from luigi import LocalTarget

from core.const import ESACPE_CHAR_FOR_NEWLINE
from core.luigi.targets import get_localtarget_path
from core.utils.pandas import convert_to_asiaseoul
from core.utils.postgres import PgConn


class BaseTask(luigi.Task):
    """ETL 시 필요한 전처리 메소드를 갖고 있는 기본 Task

    Variables:
        database (str): 데이터를 추출할 대상 Database
        table (str): 데이터를 추출할 대상 Table
        columns (list): 추출할 Table의 특정 컬럼들
            - query property가 없는 경우 위 table과 columns로 아무런 조건 없이 데이터를 조회한다.
            - query property가 있는 경우 query의 결과가 없을 때 파일로 저장할 header가 된다.
        datetime_cols (list): datetime 형식의 컬럼 지정, get_dataset 메소드에서 timezone을 바꾸는데 사용
    """
    database = None
    table = None
    columns = None
    datetime_cols = []

    @property
    def query(self):
        """특정 Query로 데이터를 가져오고 싶은 경우 특정 Query를 반환한다."""
        return None

    def get_dataset(self, database=None, table=None, columns=None, query=None):
        """pandas DataFrame으로 데이터셋을 변환한다.

        기본적으로 query property를 주 데이터셋으로 사용하고 다른 데이터셋은 Dependency로 처리한다.
        만약 여러 데이터셋이 필요하고 다른 데이터셋을 Dependency로 처리하지 않는 경우
        복잡한 Query는 query string을 인자값으로 넘겨주고 단순 Query의 경우(조건이 없는) table/columns 값을 넘겨 사용한다.
        그러나 비즈니스 로직이 들어가는 Query는 되도록 피하고 pandas로 비즈니스 로직을 구현하는 것을 원칙으로 한다.

        Args:
            database (str): 테이터베이스 명
            table (str): 테이블 명
            columns (list): 컬럼 목록
            query (str): SQL 쿼리

        Returns:
            DataFrame: 데이터셋
        """
        if not database:
            database = self.database

        if not columns:
            columns = self.columns

        # sql/table setting: query와 table 인자값에 따라 데이터셋을 생성하는 원본 소스를 다르게 가져간다.
        # table: query property 값이 있어도 table 인자값을 설정하면 설정한 테이블에서 데이터셋을 생성한다.
        _table = None
        if self.query and table:
            _table = table
        elif not self.query and table:
            _table = table
        elif not self.query and not table:
            _table = self.table  # Default

        # query: query property 보다 query 인자값이 우선순위가 높으므로 query property가 있더라도 다른 데이터셋을 생성할 수 있다.
        sql = query if query else self.query

        dataset = None
        conn = PgConn(database=database)
        with closing(conn):
            if _table:
                dataset = conn.select_all(table=_table, columns=columns, to_df=True)
            elif sql:
                dataset = conn.read_sql(sql, to_df=True)

        if not dataset.empty:
            if self.datetime_cols:
                for col in self.datetime_cols:
                    dataset[col] = dataset[col].apply(convert_to_asiaseoul)
            return dataset
        else:
            return pd.DataFrame(columns=columns)

    def convert_fileinput_to_df(self):
        """Dependency의 Output을 DataFrame으로 바꿔서 dict에 저장한다.

        LocalTarget 형태의 Output이 있는 Dependencies가 있는 경우 모든 Output을
        dict에 할당한다. Output이 list인 경우 0부터 index를 Key로 하여 할당하며
        Output이 dict인 경우 해당 Key를 Key로 하여 할당한다.

        Returns:
            (dict or None): self.input()이 있는 경우 dict로, 없는 경우 None으로 반환한다.
        """
        if self.input():
            inputs = self.input()
            converted = {}
            if isinstance(inputs, list):
                for idx, elem in enumerate(inputs):
                    if isinstance(elem, LocalTarget):
                        converted[idx] = pd.read_csv(elem.path, sep='\t')
            elif isinstance(inputs, dict):
                for key in inputs.keys():
                    if isinstance(inputs[key], LocalTarget):
                        converted[key] = pd.read_csv(inputs[key].path, sep='\t')
            else:  # single input
                if isinstance(inputs, LocalTarget):
                    converted = pd.read_csv(inputs.path, sep='\t')
            return converted
        else:
            return None

    def preprocessed_data(self):
        """전처리할 내용이 있을 경우 해당 DataFrame을 핸들링하여 반환한다."""
        df = self.get_dataset()

        return df


class LocalTargetTask(BaseTask):
    """Output이 LocalTarget인 Task"""
    subdir = None
    to_csv_header = True  # CopyToTable로 DB에 저장시킬 경우 header는 False여야 한다.

    def run(self):
        df = self.preprocessed_data()

        # 개행문자(\n)을 피하기 위해 다른 문자로 잠시 바꾸고 DB에 저장시 다시 바꿔준다.
        object_cols = []
        for col in df.columns:
            if df[col].dtype == np.object:
                object_cols.append(col)  # 문자열만 replace 가능
        df[object_cols] = df[object_cols].replace('\\n', ESACPE_CHAR_FOR_NEWLINE)

        # Convert null to None
        if self.to_csv_header:
            none_value = None
        else:
            # CopyToTable의 경우 csv 파일을 DB에 copy_from 으로 insert한다.
            # 이 떄 파일에 있는 NULL값(none_value)이라고 인식하는 값은 \N이다.
            none_value = '\\N'
        df = df.where((pd.notnull(df)), none_value)

        df.to_csv(self.output().path, index=False, encoding='utf-8',
                  header=self.to_csv_header, sep='\t')

    def output(self):
        target_dir = '{}'.format(self.get_task_namespace())
        if self.subdir:
            target_dir = '{}/{}'.format(target_dir, self.subdir)
        file = '{}.tsv'.format(self.task_id[:-11])
        path_file = get_localtarget_path(target_dir, file)

        return luigi.LocalTarget(path_file)
