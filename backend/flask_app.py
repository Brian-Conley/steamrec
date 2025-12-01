from flask import Flask
from flask_cors import CORS


# Set up the server and allow requests from the frontend container
app = Flask(__name__)
CORS(app)
