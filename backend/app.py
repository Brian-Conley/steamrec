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
        
        db.change_game_price(appid, price)

        return jsonify({
            "message": "Price updated successfully",
            "appid": appid,
            "new_price": price
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/db/insert", methods=["POST"])
def db_insert():
    try:
        appid = request.args.get("appid", type=int)
        if appid is None:
            return jsonify({"error": "Missing or invalid appid"}), 400
        
        db.insert_game_by_appid(appid)
        return jsonify({"message": "Insert successful", "appid": appid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/db/delete", methods=["DELETE"])
def db_delete():
    try:
        appid = request.args.get("appid", type=int)
        if appid is None:
            return jsonify({"error": "Missing or invalid appid"}), 400
        
        db.delete_game_by_appid(appid)

        return jsonify({
            "message": "Delete successful",
            "appid": appid
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
