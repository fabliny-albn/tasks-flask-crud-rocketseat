from flask import Flask, request, jsonify
from models.task import Task

# __name__ = "__main__"
app = Flask(__name__)

tasks = []
task_id_control = 1

# Criar uma nova task 'POST'
@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data['title'], description=data.get('description', ""))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Nova Tarefa Criada Com Sucesso!"})

# Retorna as tarefas e a quantidade de tarefas 'GET'
@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
                "tasks": task_list,
                "total_tasks": len(task_list)
            }
    
    return jsonify(output)

# Retorna tarefa específica 'GET'
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

# Altera atributos da tarefa específica 'PUT'
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    print(task)
    if task == None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    print(task)
    return jsonify({"message": "Tarefa atualizada com sucesso!", "task": task.to_dict()})

# Deleta tarefa específica 'DELETE'
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if not task:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

    tasks.remove(task)
    return jsonify({"message": "Tarefa deletada com sucesso"}), 200 


if __name__ == "__main__":
    app.run(debug=True)