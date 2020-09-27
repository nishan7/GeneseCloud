from flask import Flask, render_template, request
from db_connect import Database
app = Flask(__name__)

@app.route('/add_task', methods=['POST'])
def add_task():
    # Function used to add the task into database
    name = list(request.form.keys())[0]
    print('Created', name)
    data =db.push_data(name)
    print(data)
    return data[0], data[1], data[2]


@app.route('/set_done', methods=['POST'])
def set_done():
    # Function to set a task as completed
    id = int(list(request.form.keys())[0])
    print("Set Done", id)
    db.set_task_done(id)
    return str(id)

@app.route('/delete_task', methods=['POST'])
def delete_task():
    # Function to delete a task from database using id
    id = int(list(request.form.keys())[0])
    print('Delete', id)
    db.delete_task(id)
    return str(id)


@app.route('/')
def hello_world():
    # Main Startng Function
    data = db.get_all_data()
    return render_template('index.html',data=data)


db = Database()
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)