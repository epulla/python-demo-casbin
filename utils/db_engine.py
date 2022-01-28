from abc import ABC, abstractmethod

from sqlalchemy import create_engine

SQLITE_CONN = 'sqlite:///test.db'

class DBEngine(ABC):

    @abstractmethod
    def execute_query(self, query: str):
        pass

class SQLiteEngine(DBEngine):
    def __init__(self):
        self.conn = create_engine(SQLITE_CONN).connect()

    def execute_query(self, query):
        return self.conn.execute(query)

