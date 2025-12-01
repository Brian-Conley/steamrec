from flask import Flask, jsonify, request
import Db
from flask_app import app


@app.route("/db/insert", methods=["POST"])
def db_insert():
    try:
        appid = request.args.get("appid", type=int)
        if appid is None:
            return jsonify({"error": "Missing or invalid appid"}), 400

        Db.instance.insert_game_by_appid(appid)
        return jsonify({"message": "Insert successful", "appid": appid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
