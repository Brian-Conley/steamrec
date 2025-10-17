import sqlite3


class Db:
    def __init__(self, filename):
        self.filename = filename

    def query_game_by_appid(self, appid):
        """
        Fetch a game row by its appid

        Params:
            appid (int): Steam appid

        Returns:
            tuple: All values related to the game
        """
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            game = cur.execute(
                    "SELECT * FROM games WHERE appid = ?",
                    (appid,))
            return game.fetchone()

    def query_game_by_name(self, name):
        """
        Fetch a game row by its name

        Params:
            name (string): The game's name (partial match supported)

        Returns:
            tuple: All values related to the game
        """
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            game = cur.execute("SELECT * FROM games WHERE name LIKE ?",
                               (f"%{name}%",))
            return game.fetchall()

    def query_categories_by_appid(self, appid):
        """
        Fetch all categories associated with an appid

        Params:
            appid (int): The game's appid

        Returns:
            list: All category ids associated with the appid
        """
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            categories = cur.execute("""
                                     SELECT categoryid FROM game_categories
                                     WHERE appid = ?
                                     """, (appid,))
            cids = categories.fetchall()
            return [c[0] for c in cids]

    def query_category_by_id(self, cid):
        """
        Fetch a category name by its id

        Params:
            cid (int): The category's id

        Returns:
            string: Category name
        """
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            cat = cur.execute("SELECT name FROM categories WHERE id = ?",
                              (cid,))
            return cat.fetchone()[0]

    def query_category_by_name(self, name):
        """
        Fetch a category id by its name

        Params:
            name (string): The category's name

        Returns:
            id (int): The category's id
        """
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            cat = cur.execute("""
                              SELECT id FROM categories
                              WHERE name LIKE ?
                              """, (f"%{name}%",))
            return cat.fetchone()[0]

    def query_game_count(self):
        # Total number of games
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            count = cur.execute("SELECT COUNT(*) FROM games")
            return count.fetchone()[0]

    def query_category_count(self):
        # Total number of categories
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            count = cur.execute("SELECT COUNT(*) FROM categories")
            return count.fetchone()[0]
