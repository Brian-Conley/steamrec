import sqlite3


class Db:
    def __init__(self, filename):
        self.db = sqlite3.connect(filename)
        self.cur = self.db.cursor()
