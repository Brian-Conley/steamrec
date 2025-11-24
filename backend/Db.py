import sqlite3
import SteamStoreAPI as ssa

_filename = "steam_games.db"


class Db:
    def __init__(self, filename):
        self.filename = filename
        self.meta_tables = ['categories', 'tags', 'developers', 'publishers']

    def get_app_details(self, appid):
        game_data = self.query_game_by_appid(appid)
        if game_data is None:
            # appid doesn't exist
            return None

        category_relations = self.query_relation_by_appid('game_categories', appid)
        tag_relations = self.query_relation_by_appid('game_tags', appid)
        developer_relations = self.query_relation_by_appid('game_developers', appid)
        publisher_relations = self.query_relation_by_appid('game_publishers', appid)

        categories = self.query_items_by_id('categories', category_relations)
        if categories is None:
            categories = []
        tags = self.query_items_by_id('tags', tag_relations)
        if tags is None:
            tags = []
        developers = self.query_items_by_id('developers', developer_relations)
        if developers is None:
            developers = []
        publishers = self.query_items_by_id('publishers', publisher_relations)
        if publishers is None:
            publishers = []

        return {
                "appid": game_data[0],
                "name": game_data[1],
                "controller_support": game_data[2],
                "has_achievements": game_data[3],
                "supports_windows": game_data[4],
                "supports_mac": game_data[5],
                "supports_linux": game_data[6],
                "price": game_data[7],
                "release_date": game_data[8],
                "header_image": game_data[9],
                "positive_reviews": game_data[10],
                "negative_reviews": game_data[11],
                "total_reviews": game_data[12],
                "categories": categories,
                "tags": tags,
                "developers": developers,
                "publishers": publishers
                }

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

    def query_appid_by_name(self, name):
        """
        Fetch all appids of games matching the given name pattern

        Params:
            name (string): Game name

        Returns:
            array[int]: All appids matching the pattern
        """
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            appids = cur.execute(
                    """
                    SELECT appid FROM games
                    WHERE name LIKE ?;
                    """,
                    (f"%{name}%",)).fetchall()
            return [t[0] for t in appids] if appids else []

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

    def query_games_by_tags(self, tids, match_all=True):
        """
        Fetch every game matching the tag filters

        Params:
            tids (int[]): A list of all tag ids
            match_all (bool): Match every filter / Match any filter

        Returns:
            A list of games matching the filter
        """
        with sqlite3.connect(self.filename) as conn:
            if len(tids) == 0:
                return []
            cur = conn.cursor()
            placeholders = ','.join('?' * len(tids))
            if match_all:
                games = cur.execute(f"""
                                    SELECT DISTINCT appid
                                    FROM game_tags
                                    WHERE tid IN ({placeholders})
                                    GROUP BY appid
                                    HAVING COUNT(DISTINCT tid) = ?
                                    """, tuple(tids) + (len(tids),)).fetchall()
            else:
                games = cur.execute(f"""
                                    SELECT DISTINCT appid
                                    FROM game_tags
                                    WHERE tid IN ({placeholders})
                                    """, tuple(tids)).fetchall()
            return [appid[0] for appid in games] if games else None

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

    def query_relation_by_appid(self, table_name, appid):
        """
        Fetch all relations associated with an appid

        Params:
            table_name (string): The name of the desired relation.
                MUST be one of:
                    'game_categories', 'game_tags',
                    'game_developers', 'game_publishers'

            appid (int): The game's appid

        Returns:
            list: All relation ids associated with the appid
        """
        match table_name:
            case 'game_categories':
                idname = 'cid'
            case 'game_tags':
                idname = 'tid'
            case 'game_developers':
                idname = 'did'
            case 'game_publishers':
                idname = 'pid'
            case _:
                return None

        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()

            categories = cur.execute(f"""
                                     SELECT {idname} FROM {table_name}
                                     WHERE appid = ?
                                     """, (appid,))
            cids = categories.fetchall()
            return [c[0] for c in cids] if cids else None

    def query_items_by_id(self, table_name, id):
        """
        Fetch the name of one or more items using id(s)

        Params:
            table_name (string):
                name of one of the tables defined in self.meta_tables

            id (int or list[int]): The id(s) to look up

        Returns:
            string or list[string]: Name(s) associated with the id(s).
        """
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()

            if table_name not in self.meta_tables:
                return None

            if isinstance(id, (int, float)):
                cat = cur.execute(f"""SELECT name FROM {table_name}
                                        WHERE id = ?""",
                                  (id,)).fetchone()
                name = cat[0] if cat else None

            elif isinstance(id, list):
                placeholders = ', '.join(['?'] * len(id))
                cat = cur.execute(f"""SELECT name FROM {table_name}
                                        WHERE id IN ({placeholders})""",
                                  tuple(id),).fetchall()
                name = [n[0] for n in cat]

            else:
                name = None

            return name

    def query_item_by_name(self, table_name, name):
        """
        Fetch a category id by its name

        Params:
            table_name (string):
                name of one of the tables defined in self.meta_tables

            name (string): The item's name

        Returns:
            id (int): The item's id
        """
        if table_name not in self.meta_tables:
            return None

        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            cat = cur.execute(f"""
                              SELECT id FROM {table_name}
                              WHERE name LIKE ?
                              """, (f"%{name}%",)).fetchone()
            return cat[0] if cat else None

    def query_game_count(self):
        # Total number of games
        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            count = cur.execute("SELECT COUNT(*) FROM games")
            return count.fetchone()[0]

    def query_item_count(self, table_name):
        """
        Get the number of items in a table.

        Params:
            table_name (string):
                MUST be one of the values defined in self.meta_tables

        Returns:
            int: Number of items in the table
        """
        if table_name not in self.meta_tables:
            return None

        with sqlite3.connect(self.filename) as conn:
            cur = conn.cursor()
            count = cur.execute(f"SELECT COUNT(*) FROM {table_name}")
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
