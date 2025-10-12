import sqlite3


class Db:
    def __init__(self, filename):
        self.filename = filename

    def query_game_by_appid(self, appid):
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            game = cur.execute(
                    "SELECT * FROM Games WHERE appid = ?",
                    (appid,))
            return game.fetchall()

    def query_game_by_name(self, name):
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            game = cur.execute("SELECT * FROM Games WHERE name LIKE ?",
                               (f"%{name}%",))
            return game.fetchall()
