"""
main app 
"""
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.instance_path="/tmp"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    """ DATABASE """
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    #what should be the title and serial number 
    def __repr__(self)->str:
        return f"{self.sno}-{self.title}"

@app.route("/", methods=['GET','POST'])
def hello_world():
    
    """ Hello world """
    
    
    if request.method=='POST':
        title = (request.form['title'])
        desc = (request.form['desc'])
        todo = Todo(title=title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html',allTodo=allTodo)
    

@app.route("/delete/<int:sno>")
def delete(sno):
    """ delete """
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')



