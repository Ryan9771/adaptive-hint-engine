from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import os
from db.setup_db import get_exercise_details

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


@app.route("/exercise/:exercise_id", methods=["GET"])
def exercise(exercise_id):
    exercise = exercise.lower()

    exercise_details = get_exercise_details(
        exercise_key=exercise_id
    )

    print(f"\n== Exercise Details ==\n{exercise_details}")

    if exercise_details:
        return jsonify(exercise_details), 200

    return jsonify({"error": "Exercise not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
