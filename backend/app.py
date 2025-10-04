from flask import Flask, jsonify
from flask_cors import CORS

# Set up the server and allow requests from the frontend container
app = Flask(__name__)
CORS(app)


@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello, World!\n IF YOU CAN READ THIS IT WORKS"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
