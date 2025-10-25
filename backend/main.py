import app
import routes.hello
import routes.db.game
import routes.db.insert
import routes.db.delete
import routes.db.update


if __name__ == "__main__":
    app.app.run(host="0.0.0.0", port=5000, debug=True)
