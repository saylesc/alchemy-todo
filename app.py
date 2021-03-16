from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/udacity'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
   __tablename__ = 'todos'
   id = db.Column(db.Integer, primary_key=True)
   description = db.Column(db.String(), nullable=False)

   # Define the debug data to display
   def __repr__(self):
      return f'<TODO {self.id} {self.description}>'

# Create all tables
db.create_all()

@app.route('/')
def index():
   return render_template('index.html', data = Todo.query.all())