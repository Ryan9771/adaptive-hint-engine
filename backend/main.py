from flask import Flask, jsonify, request
from dotenv import load_dotenv

# Load Secrets
load_dotenv()

# Setup App
app = Flask(__name__)


@app.route("/")
def home():
    return "Flask app really really works on reloading!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
