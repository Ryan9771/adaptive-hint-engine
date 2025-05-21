from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import os
from db.setup_db import get_exercise_details, modify_exercise, Base, engine
from flask_cors import CORS
from agent_trials.agents.multi_agent import HintEngine
from util.types import AttemptContext
from example_exercises.python.exercise_2 import test_ex_2
import requests
import json

# Load Secrets
load_dotenv()

# Setup App
app = Flask(__name__)
CORS(app, resources={
     r"/exercise/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]

# Database
db = SQLAlchemy(app)

# Agent
agent = HintEngine()


@app.route("/")
def home():
    return "Flask app is active!"


@app.route("/exercise/<exercise_id>", methods=["POST"])
def get_exercise(exercise_id):
    try:
        print(f"\n== RETRIEVING EXERCISE ==\n{exercise_id}")
        exercise = exercise_id.lower()

        exercise_details = get_exercise_details(
            exercise_key=exercise
        )

        if exercise_details:
            return jsonify(exercise_details), 200

        return jsonify({"message": "Exercise not found"}), 404
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"message": "Cant get exercise", "details": str(e)}), 500


@app.route("/exercise/reset/<exercise_id>", methods=["POST"])
def get_reset_exercise(exercise_id):
    try:
        print(f"\n== RESETTING EXERCISE ==\n{exercise_id}")
        exercise_key = exercise_id.lower()
        exercise = get_exercise_details(exercise_key=exercise_key)

        if exercise:
            modify_exercise(exercise_key=exercise_key,
                            previous_code=exercise["skel_code"])

            return jsonify({}), 200

        print(f"\n== No exercise found with {exercise_id} ==\n")

        return jsonify({"message": f"Exercise {exercise_id} not found"}), 404

    except Exception as e:
        print(f"\n== ERROR ==\n{e}")
        return jsonify({"message": "Can't reset exercise", "details": str(e)}), 500


@app.route("/exercise/hint/<exercise_id>", methods=["POST"])
def get_exercise_hint(exercise_id):
    data = request.get_json()
    """
    Request Type:
    {
        "studentCode": string
        "error": string
        "testResults": [
            {
                "input": string
                "expected": string
                "actual": string
                "passed": string
            },
            ...
        ]
    }
    """
    try:
        print(f"\n== GETTING HINT ==\n")
        exercise_key = exercise_id.lower()

        exercise = get_exercise_details(exercise_key=exercise_key)

        if exercise:
            # Update previous_code to current code
            modify_exercise(exercise_key=exercise_id,
                            previous_code=data["studentCode"])

            test_results = "\n".join(
                [
                    f"Input: {test['input']}, Expected: {test['expected']}, Actual: {test['actual']}, Passed: {test['passed']}"
                    for test in data["testResults"]
                ]
            )

            initial_graph_state = AttemptContext(
                exercise_key=exercise_key,
                exercise_text=exercise["exercise_text"],
                skel_code=exercise["skel_code"],
                language="python",
                student_code=data["studentCode"],
                error=data["error"],
                test_results=test_results
            )

            # Get hint
            graph = agent.run(state={"attempt_context": initial_graph_state})
            print(f"\n == HINT ==\n{graph["hint_output"].hint_text}")

            return jsonify({"hint": graph["hint_output"].hint_text}), 200

        print(f"\n== Exercise {exercise_key} not found ==\n")

        return jsonify({"message": "Exercise not found"}), 404

    except Exception as e:
        print(f"\n== ERROR ==\n{e}"), 500


@app.route("/exercise/test/<exercise_id>", methods=["POST"])
def get_test(exercise_id):
    data = request.get_json()
    """
    Request Type:
    {
        "studentCode": string
    }
    """
    full_code = f"{data["studentCode"]}\n\n{test_ex_2}"
    piston_payload = {
        "language": "python",
        "version": "3.10.0",
        "files": [{"name": "main.py", "content": full_code}],
    }

    # TEST GOOGLE SHEETS PAYLOAD
    # sheets_payload = {
    #     "studentId": "ryan",
    #     "exerciseId": "patel"
    # }

    try:
        piston_response = requests.post(
            "https://emkc.org/api/v2/piston/execute", json=piston_payload)
        result = piston_response.json()

        stdout = result.get("run", {}).get("stdout", "")
        stderr = result.get("run", {}).get("stderr", "")

        # Parse only lines prefixed with the marker
        test_results = []
        for line in stdout.splitlines():
            if line.startswith("@@TEST_RESULT@@"):
                json_part = line.replace("@@TEST_RESULT@@", "").strip()
                try:
                    test_results.append(json.loads(json_part))
                except:
                    pass

        is_real_error = (
            stderr
            and not stderr.strip().startswith("...")
            and (
                "Traceback" in stderr
                or "SyntaxError" in stderr
                or "Exception" in stderr
            )
        )

        # # TEST GOOGLE SHEETS
        # response = requests.post(
        #     "https://script.google.com/macros/s/AKfycbwsJAKjKJpydZzq271dRU3vTgYXQzDh7WypQNvs1M7OXXmWpbFbDdpPXsRRuQgbRsX4TA/exec", json=sheets_payload
        # )

        return jsonify({
            "stderr": stderr if is_real_error else "",
            "testResults": test_results
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Execution failed",
            "stderr": str(e),
            "stdout": "",
            "testResults": []
        }), 500


if __name__ == "__main__":
    with app.app_context():
        Base.metadata.create_all(bind=engine)
    app.run(host="0.0.0.0", port=5001, debug=True)
