from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
from db.setup_db import get_exercise_details, Base, engine, set_previous_code, get_or_create_student_exercise, get_or_create_exercise, get_evaluation_metrics, get_test_cases, create_engine
from flask_cors import CORS
from agents.multi_agent import HintEngine
from agents.single_agent import SingleHintAgent
from util.types import AttemptContext
import requests
import json

# Load Secrets
# load_dotenv()

# Setup App
app = Flask(__name__, static_folder="../client/dist", static_url_path="/")
CORS(app, resources={
     r"/exercise/*": {"origins": ["http://localhost:5173", "https://adaptive-hint-generator-629e95ca5085.herokuapp.com/"]}}, supports_credentials=True)


# Agent
agent = HintEngine()
single_agent = SingleHintAgent()

with app.app_context():
    Base.metadata.create_all(bind=engine)


@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/exercise/<student_name>/<exercise_id>", methods=["POST"])
def get_exercise(student_name, exercise_id):
    try:
        print(f"\n== RETRIEVING EXERCISE ==\n{exercise_id}")
        exercise = exercise_id.lower()

        exercise_details = get_exercise_details(
            student_name=student_name, exercise_key=exercise
        )

        print(f"\n== EXERCISE DETAILS ==\n{exercise_details}")

        if exercise_details:
            return jsonify(exercise_details), 200

        return jsonify({"message": "Exercise not found"}), 404
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"message": "Cant get exercise", "details": str(e)}), 500


@app.route("/exercise/reset/<student_name>/<exercise_id>", methods=["POST"])
def get_reset_codebox(student_name, exercise_id):
    try:
        print(f"\n== RESETTING CODEBOX to SKELCODE ==\n{exercise_id}")
        exercise_key = exercise_id.lower()
        student_name = student_name.lower()
        student_exercise = get_or_create_student_exercise(
            student_name=student_name,
            exercise_key=exercise_key
        )
        exercise = get_or_create_exercise(exercise_key=exercise_key)

        if student_exercise:
            set_previous_code(student_name=student_name, exercise_key=exercise_key,
                              previous_code=exercise.skel_code)

            return jsonify({}), 200

        print(f"\n== No exercise found with {exercise_id} ==\n")

        return jsonify({"message": f"Exercise {exercise_id} not found"}), 404

    except Exception as e:
        print(f"\n== ERROR ==\n{e}")
        return jsonify({"message": "Can't reset exercise", "details": str(e)}), 500


@app.route("/exercise/hint/<student_name>/<exercise_id>", methods=["POST"])
def get_exercise_hint(student_name, exercise_id):
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

        exercise = get_exercise_details(
            student_name=student_name, exercise_key=exercise_key)

        if exercise:

            test_results = "\n".join(
                [
                    f"Input: {test['input']}, Expected: {test['expected']}, Actual: {test['actual']}, Passed: {test['passed']}"
                    for test in data["testResults"]
                ]
            )

            initial_graph_state = AttemptContext(
                student_name=student_name,
                exercise_key=exercise_key,
                exercise_text=exercise["exercise_text"],
                skel_code=exercise["skel_code"],
                student_code=data["studentCode"],
                error=data["error"],
                test_results=test_results
            )

            # Get multi-agent hint
            graph = agent.run(state={"attempt_context": initial_graph_state})

            # Update previous_code to current code
            set_previous_code(
                student_name=student_name,
                exercise_key=exercise_key,
                previous_code=data["studentCode"]
            )

            # Get a single-invokated llm hint
            simple_hint = single_agent.run(
                state={
                    "skel_code": exercise['skel_code'],
                    "exercise_text": exercise["exercise_text"],
                    "student_code": data["studentCode"]
                }
            )

            return jsonify({"hint": graph["hint_output"].hint_text, "simpleHint": simple_hint['hint']}), 200

        print(f"\n== Exercise {exercise_key} not found ==\n")

        return jsonify({"message": "Exercise not found"}), 404

    except Exception as e:
        print(f"\n== ERROR ==\n{e}"), 500


@app.route("/exercise/test/<student_name>/<exercise_id>", methods=["POST"])
def get_test(student_name, exercise_id):
    data = request.get_json()
    """
    Request Type:
    {
        "studentCode": string
    }
    """
    test_cases = get_test_cases(exercise_key=exercise_id.lower())
    full_code = f"{data["studentCode"]}\n\n{test_cases}"

    print(f"\n== TESTING CODE ==\n{full_code}")

    piston_payload = {
        "language": "python",
        "version": "3.10.0",
        "files": [{"name": "main.py", "content": full_code}],
    }

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


@app.route("/exercise/evaluation/<student_name>/<exercise_id>", methods=["POST"])
def get_evaluation(student_name, exercise_id):
    data = request.get_json()
    """
    Request Type:
    {
        hintRating: int
        simpleHintRating: int
        hintText: str,
        simpleHintText: str

    }

    Things to log per sheet (1 sheet -> one exercise):
    - student
    - attempt num
    - timestamp
    - concept
    - stuck count
    - hint tone
    - hint strategy
    """

    print(f"\n== GETTING EVALUATION ==\n")

    # Get metrics from db
    metrics = get_evaluation_metrics(
        student_name=student_name, exercise_key=exercise_id
    )

    combined_data = {"exerciseId": exercise_id, **data, **metrics}

    print(f"\n== EVALUATION DATA ==\n{combined_data}")

    try:
        requests.post(
            "https://script.google.com/macros/s/AKfycbwyG9CCZ4-ybTjdivbFiHyl_goa11oXKYv-MpzwkUFA9-EX1twMpn26E-qvrA-6nE6gTg/exec", json=combined_data)
        print(f"\n== EVALUATION LOGGED SUCCESSFULLY ==\n")
        return jsonify({}), 200
    except Exception as e:
        print(f"\n== ERROR LOGGING EVALUATION ==\n{e}")
        return jsonify({"message": "Error logging evaluation", "details": str(e)}), 500


if __name__ == "__main__":
    # with app.app_context():
    #     Base.metadata.create_all(bind=engine)
    app.run(host="0.0.0.0", port=5001, debug=True)
