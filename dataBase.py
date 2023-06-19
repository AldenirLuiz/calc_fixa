import sqlite3
from sqlite3 import OperationalError as Err


class DataConn:
    querys = {
        "add_data": "INSERT INTO '{}' VALUES{}",
        "create_table": "CREATE TABLE '{}' {}"
    }
    def __init__(self) -> None:
        self.db_file = "daBase.db"
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def query_add(self, table: str, data: dict):
        try:
            self.cursor.execute(self.querys["create_table"].format(table, tuple(data.keys())))
        except Err as err:
            print(err)
        
        self.cursor.execute(self.querys["add_data"].format(table, tuple(data.values())))
        self.conn.commit()
        self.conn.close()