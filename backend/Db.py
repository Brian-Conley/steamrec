import sqlite3


class Db:
    def __init__(self, filename):
        self.filename = filename

    def query_game_by_appid(self, appid):
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            game = cur.execute(
                    "SELECT * FROM games WHERE appid = ?",
                    (appid,))
            return game.fetchone()

    def query_game_by_name(self, name):
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            game = cur.execute("SELECT * FROM games WHERE name LIKE ?",
                               (f"%{name}%",))
            return game.fetchall()

    def query_categories_by_appid(self, appid):
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            categories = cur.execute("""
                                     SELECT * FROM game_categories
                                     WHERE appid = ?
                                     """, (appid,))
            return categories.fetchall()

    def query_category_by_id(self, cid):
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            cat = cur.execute("SELECT * FROM categories WHERE id = ?",
                              (cid,))
            return cat.fetchall()

    def query_category_by_name(self, name):
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            cat = cur.execute("SELECT * FROM categories WHERE name LIKE ?",
                              (f"%{name}%",))
            return cat.fetchall()
