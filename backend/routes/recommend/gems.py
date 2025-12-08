from flask import jsonify, request
import Db
import SteamWebAPI as swa
from flask_app import app
import math
from .steamid_utils import extract_steamid

@app.route("/recommend/hidden-gems", methods=["GET"])
def hidden_gems():
    raw_id = request.args.get("steamid")
    if raw_id is None:
        return jsonify({"error": "steamid not provided"}), 400

    steamid = extract_steamid(raw_id)
    if not steamid:
        return jsonify({"error": "Invalid or unresolved steamid"}), 400

    candidates = Db.instance.custom_query(
        """
        SELECT appid, positive_reviews, total_reviews
        FROM games
        WHERE total_reviews < 500 AND total_reviews > 50;
        """
    )

    gems = []
    for c in candidates:
        if (c[1] / c[2]) > 0.9:
            gems.append(c[0])

    tag_weights = {}
    tag_names = Db.instance.custom_query("SELECT name FROM tags")
    for name in tag_names:
        tag_weights[name[0]] = 0

    user_games = swa.instance.GetOwnedGames(steamid)
    if not user_games:
        return jsonify({"error": "Unable to fetch user data"}), 400

    u_games = user_games.get("games", {})

    for appid in u_games:
        playtime_hrs = u_games[appid] / 60
        game = Db.instance.get_app_details(appid)
        if not game:
            continue
        for tag in game["tags"]:
            tag_weights[tag] += math.log(1 + playtime_hrs)

    scores = {}
    for appid in gems:
        game = Db.instance.get_app_details(appid)
        if not game:
            continue
        score = sum(tag_weights[tag] for tag in game["tags"])
        scores[appid] = (score, game)

    top_50 = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)[:50]
    top_50 = [item[1][1] for item in top_50]

    return jsonify(top_50)
