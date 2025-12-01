from flask import Blueprint, request, jsonify
from SteamWebAPI import instance as steamapi
import Db
import sqlite3

sync_user_bp = Blueprint("sync_user", __name__)

DB_FILE = "steam_games.db"

def ensure_user_table():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_owned_games (
                user_id TEXT NOT NULL,
                appid INTEGER NOT NULL,
                playtime INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, appid)
            );
        """)
        conn.commit()

@sync_user_bp.route("/sync_user", methods=["POST"])
def sync_user():
    data = request.get_json(force=True)
    steamid = data.get("steamid")

    if not steamid:
        return jsonify({"error": "Missing steamid"}), 400

    ensure_user_table()

    owned = steamapi.GetOwnedGames(steamid)
    if not owned:
        return jsonify({"error": "Failed to fetch user library"}), 500

    games = owned["games"]  # dict: {appid: playtime}

    # Store user-owned games
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        for appid, playtime in games.items():
            cur.execute("""
                INSERT OR REPLACE INTO user_owned_games (user_id, appid, playtime)
                VALUES (?, ?, ?);
            """, (steamid, appid, playtime))
        conn.commit()

    # Build list of owned games with names
    owned_list = []
    for appid in games.keys():
        details = Db.instance.get_app_details(appid)
        if details is None:
            owned_list.append({
                "appid": appid,
                "name": "(Unknown Title)"
            })
        else:
            owned_list.append({
                "appid": appid,
                "name": details["name"]
            })

    return jsonify({
        "message": "User library synchronized",
        "total_games": len(games),
        "owned_games": owned_list
    })
