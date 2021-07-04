from collections import namedtuple
from contextlib import contextmanager
import logging
from os import environ
from time import sleep

import mysql.connector


# We'd like to just be able to write this but this runs into a strange
# "MySQLPrepStmt object is not subscriptable" error
# from mysql.connector.cursor import MySQLCursorNamedTuple, MySQLCursorPrepared
# class MySQLCursorNamedTuplePrepared(MySQLCursorNamedTuple, MySQLCursorPrepared):
#     pass


class _wrapnamedtuple:
    """
    This class exists because of an outstanding bug in MySQL where there is no
    cursor that handles both prepared statements and namedtuple results. See:
    https://stackoverflow.com/q/49428935
    https://bugs.mysql.com/bug.php?id=92700
    https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor.html
    """

    def __init__(self, cursor):
        self._cursor = cursor

    def _row_builder(self):
        return namedtuple('Row', self._cursor.column_names)._make

    def callproc(self, *args, **kwargs):
        return self._cursor.callproc(*args, **kwargs)

    def close(self, *args, **kwargs):
        return self._cursor.close(*args, **kwargs)

    def execute(self, *args, **kwargs):
        return self._cursor.execute(*args, **kwargs)

    def executemany(self, *args, **kwargs):
        return self._cursor.executemany(*args, **kwargs)

    def fetchone(self, *args, **kwargs):
        row = self._cursor.fetchone(*args, **kwargs)
        # print(row)
        if row is None:
            return None
        self._Row = self._row_builder()
        return self._Row(row)

    def fetchall(self, *args, **kwargs):
        rows = self._cursor.fetchall(*args, **kwargs)
        # print(rows)
        self._Row = self._row_builder()
        return [self._Row(row) for row in rows]

    def fetchmany(self, *args, **kwargs):
        rows = self._cursor.fetchmany(*args, **kwargs)
        # print(rows)
        self._Row = self._row_builder()
        return [self._Row(row) for row in rows]

    def fetchwarnings(self, *args, **kwargs):
        return self._cursor.fetchwarnings(*args, **kwargs)

    def stored_results(self, *args, **kwargs):
        return self._cursor.stored_results(*args, **kwargs)

    @property
    def column_names(self):
        return self._cursor.column_names

    @property
    def description(self):
        return self._cursor.description

    @property
    def lastrowid(self):
        return self._cursor.lastrowid

    @property
    def rowcount(self):
        return self._cursor.rowcount

    @property
    def statement(self):
        return self._cursor.statement

    @property
    def with_rows(self):
        return self._cursor.with_rows

    def __iter__(self):
        self._Row = self._row_builder()
        return self

    def __next__(self):
        nxt = self._cursor.__next__()
        # print(nxt)
        return self._Row(nxt)


class DB:
    connection = None

    @classmethod
    def connect_db(cls, max_tries=5, base_sleep_seconds=1.0):
        """
        Tries to connect to the database with increasing delays in between.
        """
        if cls.connection is not None and cls.connection.is_connected():
            return

        host = environ.get('DB_HOST')
        user = environ.get('DB_USER')
        password = environ.get('DB_PASSWORD')
        database = environ.get('DB_DATABASE')

        sleep_duration = base_sleep_seconds
        for i in range(1, max_tries+1):
            try:
                cls.connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database,
                )
                logging.info(
                    'Connected to MySQL on try %d of %d.',
                    i, max_tries,
                )
                break

            except:
                if i < max_tries:
                    logging.warning(
                        'Could not establish MySQL connection on try %d of %d, will try again after %.0f seconds.',
                        i, max_tries, sleep_duration,
                    )
                    sleep(sleep_duration)
                    sleep_duration *= 2
                else:
                    logging.error(
                        'Could not establish MySQL connection on try %d of %d.',
                        i, max_tries,
                    )
                    raise
        assert(cls.connection is not None)

    @classmethod
    @contextmanager
    def get_cursor(cls):
        cls.connect_db()
        cursor = None
        try:
            cursor = _wrapnamedtuple(cls.connection.cursor(prepared=True))
            # see commented-out block at top of file
            # cursor = connection.cursor(cursor_class=MySQLCursorNamedTuplePrepared)
            yield cursor
        finally:
            if cursor is not None:
                cursor.close()
