import logging
import psycopg
from psycopg.rows import dict_row

logger = logging.getLogger("azon_tests")


class DBClient:

    def __init__(self, conninfo):
        self.connection  = psycopg.connect(conninfo, row_factory=dict_row, autocommit=True)

    def fetch_one(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            row = cursor.fetchone()

        self._log(query, params, "1 строка" if row else "строк нет")
        return row

    def fetch_all(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        self._log(query, params, f"строк: {len(rows)}")
        return rows

    def close(self):
        self.connection.close()

    def _log(self, query, params, result):
        logger.info("SQL: %s | параметры: %s | %s", " ".join(query.split()), params, result)
