from flask import Flask,request,jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
client = MongoClient("mongodb://localhost:27017/") 
db = client["todo_db"] 
todo_collection = db["todos"] 

@app.route("/")
def todo():
    return "TO_DO"
@app.route("/add",methods=["POST"])
def add():
    data=request.get_json()
    todo = {"todo": data["todo"]}
    result = todo_collection.insert_one(todo)
    return jsonify({"message": "Todo added", "id": str(result.inserted_id)})
@app.route("/delete",methods=["POST"])
def delete():
    data=request.get_json()
    todo = {"todo": data["todo"]}
    result = todo_collection.delete_one(todo)
    return jsonify({"message": "Todo Deleted", "deleted_count": result.deleted_count})
@app.route("/get_todos", methods=["GET"])
def get_todos():
    todos = list(todo_collection.find({}, {"_id": 0, "todo": 1})) 
    return jsonify(todos)

if __name__=="__main__":
    app.run(debug=True)

