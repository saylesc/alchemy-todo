from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/udacity'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Defines the ToDo Model for our database
class Todo(db.Model):
   __tablename__ = 'todos'
   id = db.Column(db.Integer, primary_key=True)
   description = db.Column(db.String(), nullable=False)

   # Define the debug data to display
   def __repr__(self):
      return f'<TODO {self.id} {self.description}>'

# Create all tables
db.create_all()


######## APP ROUTES #######
@app.route('/')
def index():
   return render_template( 'index.html', data = Todo.query.all() )

@app.route('/todos/create-todo', methods=['POST'])
def create():
   # Get the form data here
   newTodoItem = request.get_json()['description']

   #### OLD Way using form
   # newTodoItem = request.form.get( 'description', 'New todo with no description' )

   # Try to add the TODO item. If failure, rollback and report error
   error = False
   body = {}
   try: 
      newTodo = Todo( description=newTodoItem )

      # add the new todo item to the db and commit
      db.session.add( newTodo )
      db.session.commit()
      body['description'] = newTodo.description
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
   #### OLD Way using redirect
   # Redirect to the main page
   # return redirect( url_for('index') )

   
