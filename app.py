from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple in-memory storage
tasks = []
task_id = 1

@app.route('/')
def home():
    return jsonify({
        "message": "Task Manager API",
        "endpoints": ["GET /", "GET /tasks", "POST /tasks", "DELETE /tasks/<id>"]
    })

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks, "count": len(tasks)})

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    task = {"id": task_id, "title": data['title'], "completed": False}
    tasks.append(task)
    task_id += 1
    
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)