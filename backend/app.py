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
    # Usage: http://localhost:5000/db/game?appid=X
    try:
        appid = int(request.args.get("appid"))
    except (ValueError, TypeError):
        return jsonify({"error": "Missing or invalid appid"}), 400

    game = db.query_game_by_appid(appid)
    if game is None:
        return jsonify({"error": "Appid not found"}), 404

    return jsonify(dict(zip(db.get_game_table_column_names(), game)))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
