from flask_app import app
from routes.hello import hello_bp
import routes.db.game
import routes.db.insert
import routes.db.delete
import routes.db.update
import routes.sync_user
import routes.recommend
from routes.sync_user import sync_user_bp
from routes.recommend import recommend_bp

import tarfile
import sqlite3

app.register_blueprint(sync_user_bp)
app.register_blueprint(recommend_bp)

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

if __name__ == "__main__":
    with tarfile.open("steam_games.db.tar.gz", "r:gz") as tar:
        tar.extractall(path=".")
    app.run(host="0.0.0.0", port=5000, debug=True)