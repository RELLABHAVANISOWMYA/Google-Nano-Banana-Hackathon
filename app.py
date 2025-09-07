import os
from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = "https://api.google.dev/gemini-api/v1beta/models/gemini-2.5-flash-image:generate"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    food_query = data.get("food")

    if not food_query:
        return jsonify({"error": "No food query provided"}), 400

    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    payload = {
        "prompt": f"Generate a realistic, colorful menu image of {food_query}, in hostel canteen style.",
        "size": "512x512"
    }

    response = requests.post(GEMINI_ENDPOINT, headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({"error": "API request failed", "details": response.text}), 500

    image_url = response.json().get("data", [{}])[0].get("url")
    return jsonify({"image_url": image_url})

if __name__ == "__main__":
    app.run(debug=True)
