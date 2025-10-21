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
                    (appid,)).fetchone()
            return game if game else None

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
                               (f"%{name}%",)).fetchall()
            return game if game else None

    def query_games_by_categories(self, cids, match_all=True):
        """
        Fetch every game matching the category filters

        Params:
            cids (int[]): A list of all category ids
            match_all (bool): Match every filter / Match any filter

        Returns:
            A list of games matching the filter
        """
        with sqlite3.connect(self.filename) as conn:
            if len(cids) == 0:
                return []
            cur = conn.cursor()
            placeholders = ','.join('?' * len(cids))
            if match_all:
                games = cur.execute(f"""
                                    SELECT DISTINCT appid
                                    FROM game_categories
                                    WHERE categoryid IN ({placeholders})
                                    GROUP BY appid
                                    HAVING COUNT(DISTINCT categoryid) = ?
                                    """, tuple(cids) + (len(cids),)).fetchall()
            else:
                games = cur.execute(f"""
                                    SELECT DISTINCT appid
                                    FROM game_categories
                                    WHERE categoryid IN ({placeholders})
                                    """, tuple(cids)).fetchall()
            return games if games else None

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
            return [c[0] for c in cids] if cids else None

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
                              (cid,)).fetchone()
            return cat[0] if cat else None

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
                              """, (f"%{name}%",)).fetchone()
            return cat[0] if cat else None

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

    def get_game_table_column_names(self):
        # List of the column names
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            cur.execute("PRAGMA table_info(games)")
            attributes = [row[1] for row in cur.fetchall()]
            return attributes
