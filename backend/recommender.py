import sqlite3
from collections import Counter
import math
import Db

DB_FILE = "steam_games.db"

# =========================================================
# LAZY-LOADED GAME CACHE
# =========================================================

GAME_CACHE = []
CACHE_LOADED = False


def load_all_games():
    """Load all games at once into memory for fast recommendation."""
    global GAME_CACHE

    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        rows = cur.execute("""
            SELECT
                g.appid,
                g.name,
                g.price,
                g.positive_reviews,
                g.negative_reviews,
                GROUP_CONCAT(DISTINCT c.name),
                GROUP_CONCAT(DISTINCT t.name)
            FROM games g
            LEFT JOIN game_categories gc ON g.appid = gc.appid
            LEFT JOIN categories c ON gc.cid = c.id
            LEFT JOIN game_tags gt ON g.appid = gt.appid
            LEFT JOIN tags t ON gt.tid = t.id
            GROUP BY g.appid;
        """).fetchall()

    out = []

    for row in rows:
        appid = row[0]

        categories = row[5].split(",") if row[5] else []
        tags = row[6].split(",") if row[6] else []

        out.append({
            "appid": appid,
            "name": row[1],
            "price": row[2],
            "positive_reviews": row[3] or 0,
            "negative_reviews": row[4] or 0,
            "categories": categories,
            "tags": tags
        })

    GAME_CACHE = out


def ensure_cache_loaded():
    """Ensure we only load the DB after it exists & exactly once."""
    global CACHE_LOADED
    if not CACHE_LOADED:
        load_all_games()
        CACHE_LOADED = True


# =========================================================
# USER LIBRARY
# =========================================================

def get_user_owned(steamid):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        rows = cur.execute("""
            SELECT appid
            FROM user_owned_games
            WHERE user_id = ?
        """, (steamid,)).fetchall()
    return [appid for (appid,) in rows]


# =========================================================
# REVIEW CONFIDENCE
# =========================================================

def wilson_score(pos, neg):
    n = pos + neg
    if n == 0:
        return 0.0

    z = 1.96  # 95% confidence
    phat = pos / n

    return (
        (phat + z*z/(2*n) - z * math.sqrt((phat*(1-phat) + z*z/(4*n))/n))
        / (1 + z*z/n)
    )


# =========================================================
# USER PROFILE
# =========================================================

def build_profile(steamid):
    owned = get_user_owned(steamid)

    cat_counter = Counter()
    tag_counter = Counter()

    for appid in owned:
        g = Db.instance.get_app_details(appid)
        if not g:
            continue

        cat_counter.update(g["categories"])
        tag_counter.update(g["tags"])

    total_cat = sum(cat_counter.values()) or 1
    total_tag = sum(tag_counter.values()) or 1

    profile_cats = {k: v / total_cat for k, v in cat_counter.items()}
    profile_tags = {k: v / total_tag for k, v in tag_counter.items()}

    return {
        "categories": profile_cats,
        "tags": profile_tags,
    }


# =========================================================
# SCORING FUNCTION
# =========================================================

def compute_score(profile, game):

    # Weighted category matching
    category_score = sum(
        profile["categories"].get(cat, 0)
        for cat in game["categories"]
    )

    # Weighted tag matching
    tag_score = sum(
        profile["tags"].get(tag, 0)
        for tag in game["tags"]
    )

    # Review confidence
    pos = game["positive_reviews"]
    neg = game["negative_reviews"]
    review = wilson_score(pos, neg)

    # Weighted total
    return (
        0.40 * category_score +
        0.50 * tag_score +
        0.10 * review
    )


# =========================================================
# MAIN RECOMMENDER
# =========================================================

def recommend_for_user(steamid, limit=10):

    # Load the DB cache only when needed
    ensure_cache_loaded()

    profile = build_profile(steamid)
    owned = set(get_user_owned(steamid))

    # Exclude owned games
    candidates = [
        g for g in GAME_CACHE
        if g["appid"] not in owned
    ]

    scored = []

    for g in candidates:
        score = compute_score(profile, g)
        scored.append({
            "appid": g["appid"],
            "name": g["name"],
            "price": g["price"],
            "tags": g["tags"],
            "score": round(score, 4)
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:limit]
