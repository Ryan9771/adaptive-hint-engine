from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import os
from setup_db import get_exercise_details

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


@app.route("/exercise/<string:language>/<string:exercise>", methods=["GET"])
def exercise(language, exercise):
    language = language.lower()
    exercise = exercise.lower()

    exercise_details = get_exercise_details(
        exercise_key="_".join([language, exercise])
    )

    print(exercise_details)

    return f"Exercise: {exercise} in {language}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
