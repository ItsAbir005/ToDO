import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB Connection
# It attempts to get the MongoDB URI from environment variables first.
# This is crucial for deployment on platforms like Render.
# If the environment variable isn't set (e.g., during local development),
# it falls back to a localhost connection.
mongo_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)

# Specify your database name. MongoDB will create it if it doesn't exist on first write.
db = client["todo_db"]
todo_collection = db["todos"]

# Routes
@app.route("/")
def home(): # Changed function name from 'todo' to 'home' to avoid confusion, though 'todo' works too.
    return "TO_DO API is running!"

@app.route("/add", methods=["POST"])
def add_todo():
    data = request.get_json()
    if not data or "todo" not in data:
        return jsonify({"message": "Invalid request: 'todo' field is missing"}), 400

    todo_item = {"todo": data["todo"]}
    result = todo_collection.insert_one(todo_item)
    return jsonify({"message": "Todo added successfully", "id": str(result.inserted_id)}), 201

@app.route("/delete", methods=["POST"])
def delete_todo():
    data = request.get_json()
    if not data or "todo" not in data:
        return jsonify({"message": "Invalid request: 'todo' field is missing"}), 400

    todo_item = {"todo": data["todo"]}
    result = todo_collection.delete_one(todo_item)
    if result.deleted_count == 0:
        return jsonify({"message": "Todo not found"}), 404
    return jsonify({"message": "Todo deleted successfully", "deleted_count": result.deleted_count})

@app.route("/get_todos", methods=["GET"])
def get_all_todos():
    # Retrieve all todos, excluding the MongoDB '_id' field and including only the 'todo' field.
    todos = list(todo_collection.find({}, {"_id": 0, "todo": 1}))
    return jsonify(todos)

# Entry point for the Flask application
# End of app.py file
# This block is primarily for local development.
# For deployment on Render, Gunicorn will be used to run 'app:app'.
if __name__ == "__main__":
    app.run(debug=True) # debug=True is good for local development, shows error messages.
