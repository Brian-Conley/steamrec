from flask import jsonify, request
import Db
import SteamWebAPI as swa
from flask_app import app
import math


@app.route("/recommend/hidden-gems", methods=["GET"])
def hidden_gems():
    # Usage: http://localhost:5000/recommend/hidden-gems?steamid=id
    steamid = request.args.get("steamid")
    if steamid is None:
        return jsonify({"error": "steamid not provided"}), 400
    try:
        steamid = int(steamid)
    except ValueError:
        return jsonify({"error": "The steamid provided is invalid"}), 400

    # Find all hidden gems
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

    # Get tag names
    tag_weights = {}
    tag_names = Db.instance.custom_query('SELECT name FROM tags')
    for name in tag_names:
        tag_weights[name[0]] = 0

    # Get user's games
    user_games = swa.instance.GetOwnedGames(steamid)
    if not user_games:
        return jsonify({"error": "Unable to fetch user data"}), 400
    u_games = user_games.get("games", {})

    # Calculate tag weights
    for appid in u_games:
        playtime_hrs = u_games[appid] / 60
        game = Db.instance.get_app_details(appid)
        if not game:
            continue
        for tag in game["tags"]:
            tag_weights[tag] += math.log(1 + playtime_hrs)

    # Score each gem
    scores = {}
    for appid in gems:
        game = Db.instance.get_app_details(appid)
        if not game:
            continue
        score = 0
        for tag in game["tags"]:
            score += tag_weights[tag]
        scores[appid] = (score, game)
    top_50 = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)[:50]
    top_50 = [t[1][1] for t in top_50]

    return jsonify(top_50)
