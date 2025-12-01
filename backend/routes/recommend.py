from flask import Blueprint, request, jsonify
from recommender import recommend_for_user

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/recommend", methods=["GET"])
def recommend():
    steamid = request.args.get("steamid")

    if not steamid:
        return jsonify({"error": "Missing steamid"}), 400

    try:
        results = recommend_for_user(steamid)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(results)
