from flask import Flask, jsonify, request
from flask_cors import CORS
import Db
from flask_app import app


@app.route("/db/game")
def db_game():
    # Usage: http://localhost:5000/db/game?appid=X
    try:
        appid = int(request.args.get("appid"))
    except (ValueError, TypeError):
        return jsonify({"error": "Missing or invalid appid"}), 400

    game = Db.instance.query_game_by_appid(appid)
    if game is None:
        return jsonify({"error": "Appid not found"}), 404

    return jsonify(dict(zip(Db.instance.get_game_table_column_names(), game)))
