import sqlite3


class Db:
    def __init__(self, filename):
        self.db = sqlite3.connect(filename)
        self.cur = self.db.cursor()

    def query_game_by_appid(self, appid):
        game = self.cur.execute(f"SELECT * FROM Games WHERE appid={appid}")
        return game.fetchone()
