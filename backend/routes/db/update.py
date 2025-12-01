from flask import Flask, jsonify, request
import Db
from flask_app import app


@app.route("/db/update", methods=["PUT"])
def db_update():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        appid = data.get("appid")
        price = data.get("price")

        if appid is None or price is None:
                return jsonify({"error": "Missing 'appid' or 'price' in JSON"}), 400

        # Type checks
        try:
            appid = int(appid)
            price = int(price)
        except (ValueError, TypeError):
            return jsonify({"error": "'appid' and 'price' must be integers"}), 400

        if price < 0:
            return jsonify({"error": "'price' must be >= 0 (in cents)"}), 400

        Db.instance.change_game_price(appid, price)

        return jsonify({
            "message": "Price updated successfully",
            "appid": appid,
            "new_price": price
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

