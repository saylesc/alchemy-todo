from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/udacity'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Defines the TodoList (parent of Todo's) Model for our database
class TodoList(db.Model):
   __tablename__= 'todolist'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(), nullable=False)
   completed = db.Column(db.Boolean, nullable=False, default=False)
   todos = db.relationship(
      'Todo', 
      backref='todo_list', 
      lazy=True)
      # collection_class='list',
      # cascade='save-update')

   # Define the debug data to display
   def __repr__(self):
      return f'<TodoList {self.id} {self.name}>'

# Defines the ToDo Model for our database
class Todo(db.Model):
   __tablename__ = 'todos'
   id = db.Column(db.Integer, primary_key=True)
   description = db.Column(db.String(), nullable=False)
   completed = db.Column(db.Boolean, nullable=False, default=False)
   todolist_id = db.Column(
      db.Integer, 
      db.ForeignKey('todolist.id'),
      nullable=False)
   
   # Add new todos and associate them with a list as follows:
   # list = TodoList(name='My List')
   # todo = Todo(description='My Todo Item')
   # ...
   # todo.todo_list = list
   # db.session.add(list) - takes care of cascading the child todos
   # db.session.commit()

   # Define the debug data to display
   def __repr__(self):
      return f'<TODO {self.id} {self.description}, list {self.todolist_id}>'

# Create all tables
# Learned how to use migration, so this command is no longer needed
#     Instead we use 'flask db init/migrate/upgrade/downgrade'
# db.create_all()

######## APP ROUTES #######
@app.route('/todos/create-todolist', methods=['POST'])
def createList():
   # Get the form data here
   newTodoList = request.get_json()['listName']

   # Try to add the TODO List. If failure, rollback and report error
   error = False
   body = {}
   try:
      newList = TodoList( name=newTodoList )
      db.session.add( newList )
      db.session.commit()

      body['listName'] = newList.name
      body['listId'] = newList.id
   except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
   finally:
      db.session.close()
   
   if error:
      # Throw an HTTP Exception
      abort(500)
   else:
      return jsonify(body)


@app.route('/todos/create-todo', methods=['POST'])
def create():
   # Get the form data here
   newTodoItem = request.get_json()['description']
   listId = request.get_json()['listId']

   # Try to add the TODO item. If failure, rollback and report error
   error = False
   body = {}
   try: 
      newTodo = Todo( description=newTodoItem )
      newTodo.todolist_id = listId

      # add the new todo item to the db and commit
      db.session.add( newTodo )
      db.session.commit()

      # append the todo item to the return body
      body['description'] = newTodo.description
      body['id'] = newTodo.id
      body['completed'] = newTodo.completed
   except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
   finally:
      db.session.close()
   
   if error:
      # Throw an HTTP Exception
      abort(500)
   else:
      return jsonify(body)

@app.route('/todos/list/<list_id>/set-completed', methods=['POST'])
def setListComplete(list_id):
   error = False
   try:
      completed = request.get_json()['completed']
      completeList = TodoList.query.get(list_id)
      completeList.completed = completed

      if completed:
         print("Completed")
      else:
         print("Not Completed")
      
      # Also mark the children complete
      print("Deleting children for list:" + list_id)
      todos = Todo.query.filter_by(todolist_id=list_id).all()
      for todo in todos:
         print("Todo Item" + todo.description)
         todo.completed = completed
      
      db.session.commit()
      
   except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
   finally:
      db.session.close()

   if error:
      abort(500)
   else:
      return redirect(url_for('index'))

@app.route('/todos/delete-list/<list_id>', methods=['DELETE'])
def deleteList(list_id):
   error = False
   try:
      # First delete the children
      print("Deleting children for list:" + list_id)
      Todo.query.filter_by(todolist_id=list_id).delete()

      # Now delete the parent
      TodoList.query.filter_by(id=list_id).delete()

      db.session.commit()
   except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
   finally:
      db.session.close()

   if error:
      abort(500)
   else:
      return jsonify({ 'success': True })

@app.route('/todos/delete-todo/<todo_id>', methods=['DELETE'])
def deleteTodo(todo_id):
   error = False
   try:
      Todo.query.filter_by(id=todo_id).delete()
      db.session.commit()
   except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
   finally:
      db.session.close()

   if error:
      abort(500)
   else:
      return jsonify({ 'success': True })

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
   return render_template( 
      'index.html', 
      lists = TodoList.query.all(),
      active_list = TodoList.query.get(list_id),
      todos = Todo.query.filter_by(todolist_id=list_id).order_by('id')
      .all()
   )

@app.route('/')
def index():
   return redirect(url_for('get_list_todos', list_id=1))