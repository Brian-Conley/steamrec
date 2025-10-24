import sqlite3
import SteamStoreAPI as ssa

_filename = "steam_games.db"


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

    def insert_game_by_appid(self, appid):
        app = ssa.get_steam_app_details(appid)

        if not app:
            print("Invalid response")
            return -1 # Invalid response

        appdata = app.get(str(appid))
        if not appdata or not appdata.get("success"):
            return -2 # App does not exist

        appdata = appdata.get("data")
        if appdata.get("type") != "game":
            return -3 # Not a game

        info = {
            "name": appdata.get("name"),
            "controller_support": appdata.get("controller_support", None),
            "has_achievements": True if appdata.get("achievements") else False,
            "supports_windows": appdata.get("platforms", {}).get("windows", False),
            "supports_mac": appdata.get("platforms", {}).get("mac", False),
            "supports_linux": appdata.get("platforms", {}).get("linux", False),
            "price": appdata.get("price_overview", {}).get("initial", 0),
            "total_recommendations": appdata.get("recommendations", {}).get("total", 0),
            "release_date": appdata.get("release_date", {}).get("date"),
            "header_image": appdata.get("header_image"),
        }

        supp = info["controller_support"]
        if supp == "none":
            supp = 0
        elif supp == "partial":
            supp = 1
        elif supp == "full":
            supp = 2
        else:
            supp = 3

        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            cur.execute("""
                        INSERT OR REPLACE INTO games (
                            appid, name, controller_support, has_achievements,
                            supports_windows, supports_mac, supports_linux,
                            price, total_recommendations, release_date,
                            header_image
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                        appid,
                        info["name"],
                        supp,
                        info["has_achievements"],
                        info["supports_windows"],
                        info["supports_mac"],
                        info["supports_linux"],
                        info["price"],
                        info["total_recommendations"],
                        info["release_date"],
                        info["header_image"],
                        ))
            conn.commit()
            return 0  # success

    def delete_game_by_appid(self, appid):
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM games WHERE appid = ?", (appid,))
            conn.commit()

    def change_game_price(self, appid, price):
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            cur.execute("UPDATE games SET price = ? WHERE appid = ?",
                        (price, appid,))
            conn.commit()


instance = Db(_filename)
