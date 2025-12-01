from flask import jsonify
import Db
from flask_app import app


@app.route("/recommend/hidden-gems")
def hidden_gems():
    # Usage: http://localhost:5000/recommend/hidden-gems
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
            gems.append(c)
    gems.sort(reverse=True, key=lambda g: (g[1]**2) / g[2])
    gems = gems[:50]
    results = [Db.instance.get_app_details(app[0]) for app in gems]

    return jsonify(results)
