from flask import Blueprint, request, jsonify
import Db
import sqlite3

search_bp = Blueprint("search_bp", __name__)

@search_bp.route("/db/search", methods=["GET"])
def search():
    name = request.args.get("name")
    developer = request.args.get("developer")
    publisher = request.args.get("publisher")
    category = request.args.get("category")
    tags = request.args.get("tags")
    price_min = request.args.get("price_min")
    price_max = request.args.get("price_max")

    sql = """
        SELECT g.appid
        FROM games g
    """

    params = []
    joins = []
    wheres = []

    # ------------------------------
    # NAME
    # ------------------------------
    if name:
        wheres.append("g.name LIKE ?")
        params.append(f"%{name}%")

    # ------------------------------
    # DEVELOPER
    # ------------------------------
    if developer:
        joins.append("JOIN game_developers gd ON gd.appid = g.appid")
        joins.append("JOIN developers d ON d.id = gd.did")
        wheres.append("d.name LIKE ?")
        params.append(f"%{developer}%")

    # ------------------------------
    # PUBLISHER
    # ------------------------------
    if publisher:
        joins.append("JOIN game_publishers gp ON gp.appid = g.appid")
        joins.append("JOIN publishers p ON p.id = gp.pid")
        wheres.append("p.name LIKE ?")
        params.append(f"%{publisher}%")

    # ------------------------------
    # CATEGORY
    # ------------------------------
    if category:
        categories = [c.strip() for c in category.split(",")]
        joins.append("JOIN game_categories gc ON gc.appid = g.appid")
        joins.append("JOIN categories c ON c.id = gc.cid")
        wheres.append(
            "c.name IN (%s)" % ",".join("?" for _ in categories)
        )
        params.extend(categories)

    # ------------------------------
    # TAGS
    # ------------------------------
    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        joins.append("JOIN game_tags gt ON gt.appid = g.appid")
        joins.append("JOIN tags t ON t.id = gt.tid")
        wheres.append(
            "t.name IN (%s)" % ",".join("?" for _ in tag_list)
        )
        params.extend(tag_list)

    # ------------------------------
    # PRICE
    # ------------------------------
    if price_min:
        wheres.append("g.price >= ?")
        params.append(int(price_min))

    if price_max:
        wheres.append("g.price <= ?")
        params.append(int(price_max))

    # ------------------------------
    # BUILD SQL
    # ------------------------------
    if joins:
        sql += " " + " ".join(joins)

    if wheres:
        sql += " WHERE " + " AND ".join(wheres)

    sql += " GROUP BY g.appid LIMIT 200;"

    # ------------------------------
    # EXECUTE SQL (NO custom_query!)
    # ------------------------------
    db = sqlite3.connect("steam_games.db")
    cur = db.cursor()
    rows = cur.execute(sql, params).fetchall()
    db.close()

    if not rows:
        return jsonify([])

    # ------------------------------
    # RETURN GAME DETAILS
    # ------------------------------
    results = []
    for (appid,) in rows:
        details = Db.instance.get_app_details(appid)
        if details:
            results.append(details)

    return jsonify(results)
