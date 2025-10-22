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
        if appid is None:
                return jsonify({"error": "Missing appid"}), 400
        
        update_fields = {k: v for k, v in data.items() if k != "appid"}
        if not update_fields:
            return jsonify({"error": "No fields provided to update"}), 400
        
        # TODO: replace this print with the real call, e.g.
        # result = db_update_game(appid, update_fields)
        print(f"[DEBUG] Would UPDATE appid={appid} with data:\n{update_fields}")

        return jsonify({
            "message": "Update successful (test)",
            "appid": appid,
            "updated_fields": update_fields
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/db/insert", methods=["POST"])
def db_insert():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Missing json details"}), 400
        
        required_fields = [ 
            "appid", "name", "price", "release_date",
            "supports_linux", "supports_mac", "supports_windows"
        ]
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({"error": f"Missing required fields: {missing}"}), 400
        
        # TODO: Replace with db call
        # result = db.insert_game(data)
        print(f"[DEBUG] Would INSERT new game into DB:\n{data}")

        return jsonify({"message": "Insert successful (test)", "inserted": data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/db/delete", methods=["DELETE"])
def db_delete():
    try:
        appid = request.args.get("appid", type=int)
        if appid is None:
            return jsonify({"error": "Missing or invalid appid"}), 400
        
        print(f"[DEBUG] Would DELETE game with appid={appid}")
        # TODO: db.delete_game(appid)
        return jsonify({"message": "Delete successful (test)", "appid": appid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
