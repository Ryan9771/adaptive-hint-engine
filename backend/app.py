from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import os

# Load Secrets
load_dotenv()

print(os.environ["SQLALCHEMY_DATABASE_URI"])
# Setup App
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
db = SQLAlchemy(app)

# Database


@app.route("/")
def home():
    return "Flask app really really works on reloading!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
