import app
import routes.hello
import routes.db.game
import routes.db.insert
import routes.db.delete
import routes.db.update
import tarfile


if __name__ == "__main__":
    with tarfile.open("steam_games.db.tar.gz", "r:gz") as tar:
        tar.extractall(path=".")
    app.app.run(host="0.0.0.0", port=5000, debug=True)
