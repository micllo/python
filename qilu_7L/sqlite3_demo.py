import sqlite3


class SQLite:

    def __init__(self, path):
        self.path = path
        self.con = sqlite3.connect(self.path)
        self.cursor = self.con.cursor()  # 游标

    def __del__(self):
        self.con.close()

    def exec(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert(self, sql):
        self.cursor.execute(sql)
        self.cursor.commit()


if __name__ == "__main__":

    s = SQLite("/Users/micllo/Documents/七录/lib/db.sqlite3")
    print(s.exec("select * from infos"))




