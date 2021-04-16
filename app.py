from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['BUNDLE_ERRORS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
db = SQLAlchemy(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


class ListToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    status = db.Column(db.Boolean, default=False)


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('task', action='append', required=True)
{
    "message": {
        "task": "Task is required"
    }
}


resource_file = {
    'name': fields.String,
    'status': fields.Boolean,
}


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    @marshal_with(resource_file)
    def get(self, todo_id):
        return ListToDo.query.all()

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        arg = parser.parse_args()
        print(arg)
        return TODOS

    def post(self):
        args = parser.parse_args()
        print(args)
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':
    db.create_all()
    new_todo = ListToDo(name='Nau an')
    new_todo1 = ListToDo(name='Choi co')
    db.session.add(new_todo)
    db.session.add(new_todo1)
    db.session.commit()
    app.run(debug=True, port=5001)