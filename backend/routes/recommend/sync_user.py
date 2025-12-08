from flask import Blueprint, request, jsonify
from SteamWebAPI import instance as steamapi
import Db
import sqlite3
import re

sync_user_bp = Blueprint("sync_user", __name__)

DB_FILE = "steam_games.db"

def extract_steamid(raw):
    raw = str(raw).strip()

    if "steamcommunity.com" in raw:
        m = re.search(r"profiles/(\d+)", raw)
        if m:
            return m.group(1)

        m = re.search(r"id/([^/]+)", raw)
        if m:
            vanity = m.group(1)
            return resolve_vanity(vanity)

    if raw.isdigit():
        num = int(raw)
        if num > 76561197960265728:
            return str(num)
        return str(num + 76561197960265728)

    m = re.search(r"\[U:1:(\d+)\]", raw)
    if m:
        steam32 = int(m.group(1))
        return str(steam32 + 76561197960265728)

    m = re.search(r"STEAM_[0-5]:([0-1]):(\d+)", raw)
    if m:
        y = int(m.group(1))
        z = int(m.group(2))
        steam32 = z * 2 + y
        return str(steam32 + 76561197960265728)

    resolved = resolve_vanity(raw)
    if resolved:
        return resolved
    return None


def resolve_vanity(name):
    try:
        resp = steamapi.ResolveVanityURL(name)
    except Exception:
        return None

    if isinstance(resp, str):
        if resp.isdigit() and len(resp) >= 16:
            return resp
        return None

    if isinstance(resp, dict):
        if "response" in resp:
            resp = resp["response"]
        if resp.get("success") != 1:
            return None
        return resp.get("steamid")

    return None


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
    raw_id = data.get("steamid")

    if not raw_id:
        return jsonify({"error": "Missing steamid"}), 400

    steamid = extract_steamid(raw_id)
    if not steamid:
        return jsonify({"error": "Could not resolve SteamID"}), 400

    ensure_user_table()

    owned = steamapi.GetOwnedGames(steamid)
    if not owned:
        return jsonify({"error": "Failed to fetch user library"}), 500

    games = owned["games"]

    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        for appid, playtime in games.items():
            cur.execute("""
                INSERT OR REPLACE INTO user_owned_games (user_id, appid, playtime)
                VALUES (?, ?, ?);
            """, (steamid, appid, playtime))
        conn.commit()

    owned_list = []
    for appid in games.keys():
        details = Db.instance.get_app_details(appid)
        owned_list.append({
            "appid": appid,
            "name": details["name"] if details else "(Unknown Title)"
        })

    return jsonify({
        "message": "User library synchronized",
        "steamid": steamid,
        "total_games": len(games),
        "owned_games": owned_list
    })
