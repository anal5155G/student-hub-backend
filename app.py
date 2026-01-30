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
if not MONGO_URI:
    raise Exception("MONGO_URI not found! Add it in Render Environment Variables.")

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
# ROUTE: BOOK / CONTACT FORM
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

    try:
        collection.insert_one(document)
        return jsonify({"message": "Your message was saved successfully ✅"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------
# TEST MONGODB CONNECTION
# -----------------------
@app.route("/test-db")
def test_db():
    try:
        collection.insert_one({"test": "MongoDB connected"})
        return jsonify({"status": "success", "message": "MongoDB connected 🎉"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# -----------------------
# RUN SERVER
# -----------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
