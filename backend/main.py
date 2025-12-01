from flask_app import app

# Blueprints
from routes.hello import hello_bp
from routes.recommend.sync_user import sync_user_bp
from routes.recommend.recommender import recommend_bp

# DB-related routes
import routes.db.game
import routes.db.insert
import routes.db.delete
import routes.db.update
import routes.recommend.gems

import tarfile
import sqlite3


# ---------------------------
# Ensure user table exists
# ---------------------------
def ensure_user_table():
    conn = sqlite3.connect("steam_games.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_owned_games (
            user_id TEXT NOT NULL,
            appid INTEGER NOT NULL,
            playtime INTEGER,
            PRIMARY KEY (user_id, appid),
            FOREIGN KEY(appid) REFERENCES games(appid)
        );
    """)
    conn.commit()
    conn.close()

ensure_user_table()


# ---------------------------
# Register blueprints
# ---------------------------
app.register_blueprint(hello_bp)
app.register_blueprint(sync_user_bp)
app.register_blueprint(recommend_bp)


# ---------------------------
# Run server
# ---------------------------
if __name__ == "__main__":
    # Extract DB if needed
    with tarfile.open("steam_games.db.tar.gz", "r:gz") as tar:
        tar.extractall(path=".")

    app.run(host="0.0.0.0", port=5000, debug=True)
