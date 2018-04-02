def _crud_condition(series):
    """internal use only
    Set CRUD code according to condition
    :param series: pandas.Series
    :return: 'C', 'U', 'D'
    """
    import pandas as pd

    if pd.isnull(series[1]):
        return 'D'
    elif pd.isnull(series[7]):
        return 'C'
    elif not pd.isnull(series[1]) and not pd.isnull(series[7]):
        return 'U'


def set_crud_mode(df):
    """
    pandas DataFrame에 CRUD Code 컬럼 생성
    :param df: pandas DataFrame
    :return: DataFrame
    """
    df['crud_code'] = df.apply(lambda x: _crud_condition(x), axis=1)
    return df


class InvalidArguments(Exception):
    pass


def existed(db_conn=None,
            table_name=None,
            key_cols=None,
            key_vals=None) -> bool:
    """
    중복 검사
    :param db_conn: database connection
    :param table_name: table name
    :param key_cols: tuple
    :param key_vals: tuple
    :return: True or False
    """
    if None in (db_conn, table_name, key_cols, key_vals):
        msg = 'None Arguments'
        raise InvalidArguments(msg)

    if not isinstance(key_cols, tuple) or \
            not isinstance(key_vals, tuple):
        msg = 'key cols or key vals Not a Tuple'
        raise InvalidArguments(msg)

    query = "SELECT * FROM %s" % table_name
    query += " WHERE "

    for idx, key_col in enumerate(key_cols, start=1):
        query += "{0}=%s".format(key_col)
        if idx != len(key_cols):
            query += " AND "

    duplicated = list(db_conn.select(query, key_vals))
    if duplicated:
        return True
    else:
        return False
