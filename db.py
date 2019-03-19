class InvalidArguments(Exception):
    pass


def existed(db_conn=None,
            table_name=None,
            key_cols=None,
            key_vals=None) -> bool:
    """데이터의 중복을 검사한다.

    Parameters:
        db_conn (connection of psycopg2): Connection Object
        table_name (str): Table name
        key_cols (tuple): 중복을 판단할 키 컬럼
        key_vals (tuple): 중복을 판단할 키 컬럼의 값

    Returns:
        True if duplicated else False
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
