from flask import Flask, jsonify, request
from flask_cors import CORS
import app


@app.app.route("/api/hello")
def hello():
    return jsonify(
            {"message": "Hello, World!\n IF YOU CAN READ THIS IT WORKS"}
            )

