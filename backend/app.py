from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import os
from db.setup_db import get_exercise_details, modify_exercise
from flask_cors import CORS

# Load Secrets
load_dotenv()

print(os.environ["SQLALCHEMY_DATABASE_URI"])
# Setup App
app = Flask(__name__)
CORS(app, resources={
     r"/exercise/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
db = SQLAlchemy(app)


# Database


@app.route("/")
def home():
    return "Flask app really really works on reloading!"


@app.route("/exercise/<exercise_id>", methods=["POST"])
def exercise(exercise_id):
    try:
        print(f"\n== RETRIEVING EXERCISE ==\n{exercise_id}")
        exercise = exercise_id.lower()

        exercise_details = get_exercise_details(
            exercise_key=exercise
        )

        if exercise_details:
            return jsonify(exercise_details), 200

        return jsonify({"error": "Exercise not found"}), 404
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Cant get exercise", "details": str(e)}), 500


@app.route("/exercise/reset/<exercise_id>", methods=["POST"])
def reset_exercise(exercise_id):
    try:
        print(f"\n== RESETTING EXERCISE ==\n{exercise_id}")
        exercise_key = exercise_id.lower()
        exercise = get_exercise_details(exercise_key=exercise_key)

        if exercise:
            modify_exercise(exercise_key=exercise_key,
                            previous_code=exercise["skel_code"])
        else:
            print(f"\n== No exercise found with {exercise_id} ==\n")

        return jsonify({}), 200
    except Exception as e:
        print(f"\n== ERROR ==\n{e}")
        return jsonify({"error": "Can't reset exercise", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
