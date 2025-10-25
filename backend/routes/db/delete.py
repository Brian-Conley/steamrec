from flask import Flask, jsonify, request
from flask_cors import CORS
import Db
import app


@app.app.route("/db/delete", methods=["DELETE"])
def db_delete():
    try:
        appid = request.args.get("appid", type=int)
        if appid is None:
            return jsonify({"error": "Missing or invalid appid"}), 400

        Db.instance.delete_game_by_appid(appid)

        return jsonify({
            "message": "Delete successful",
            "appid": appid
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
