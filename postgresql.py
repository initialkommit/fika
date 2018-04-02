import os
from configparser import ConfigParser

import psycopg2
from psycopg2.extras import RealDictCursor


class PostgresUtil:
    def __init__(self, section='crawler', autocommit=True, autoconnect=True):
        self.conn = None
        self.cursor = None
        self.section = section
        self.autocommit = autocommit
        if autoconnect:
            self.connect()

    def config(self):
        parser = ConfigParser()
        parser.read(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)), '../', 'db.ini'))

        db = {}
        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section %s not found in the file' % self.section)

        return db

    @staticmethod
    def addslashes(field):
        return field.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"')

    def connect(self):
        params = self.config()

        # log.info('Connecting to the PostgreSQL database - %s' % self.section)
        self.conn = psycopg2.connect(**params)
        self.conn.autocommit = self.autocommit
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def select(self, query, *args, **kwargs):
        self.cursor.execute(query, *args, **kwargs)
        while True:
            row = self.cursor.fetchone()
            if not row:
                break
            yield row

    def execute(self, query, *args, **kwargs):
        self.cursor.execute(query, *args, **kwargs)

    def execute_many(self, query, *args, **kwargs):
        """
        example)
        namedict = ({"first_name":"Joshua", "last_name":"Drake"},
                    {"first_name":"Steven", "last_name":"Foo"},
                    {"first_name":"David", "last_name":"Bar"})
        """
        self.cursor.executemany(query, *args, **kwargs)

    def __del__(self):
        if self.cursor:
            self.conn.close()


if __name__ == '__main__':
    postgres = PostgresUtil()

    query = "INSERT INTO test_users(handle, name) VALUES ('test', 'test') RETURNING 1"
    print(postgres.execute(query))
