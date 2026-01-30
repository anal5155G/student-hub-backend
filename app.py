import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

# -----------------------
# CONNECT TO MONGODB ATLAS
# -----------------------
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["student_hub"]
collection = db["student_details"]

# -----------------------
# ROUTE: HOME PAGE
# -----------------------
@app.route("/")
def home():
    return "Backend is running 🚀"

# -----------------------
# ROUTE: CONTACT FORM
# -----------------------
@app.route("/book", methods=["POST"])
def book():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    document = {
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "message": data.get("message"),
        "submitted_at": datetime.utcnow()
    }

    collection.insert_one(document)
    return jsonify({"message": "Your message was saved successfully ✅"})
