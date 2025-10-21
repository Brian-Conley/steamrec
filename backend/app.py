from flask import Flask, jsonify, request
from flask_cors import CORS
import Db

db = Db.Db("steam_games.db")

# Set up the server and allow requests from the frontend container
app = Flask(__name__)
CORS(app)


@app.route("/api/hello")
def hello():
    return jsonify(
            {"message": "Hello, World!\n IF YOU CAN READ THIS IT WORKS"}
            )


@app.route("/db/game")
def db_game():
    try:
        appid = int(request.args.get("appid"))
    except (ValueError, TypeError):
        return jsonify({"error": "Missing or invalid appid"}), 400

    game = db.query_game_by_appid(appid)
    if game is None:
        return jsonify({"error": "Appid not found"}), 404

    keys = [
        "appid",
        "name",
        "controller_support",
        "has_achievements",
        "supports_windows",
        "supports_mac",
        "supports_linux",
        "price",
        "total_recommendations",
        "release_date",
        "header_image"
    ]

    return jsonify(dict(zip(keys, game)))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
