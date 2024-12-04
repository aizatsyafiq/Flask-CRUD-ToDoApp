#import 
from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, UTC

#init app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now(UTC))

    def __repr__(self) -> str:
        return f"Task {self.id}"

#route - index
@app.route('/',methods=['POST','GET'])
def index():
    #Add task
    if request.method == 'POST':
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error: {e}"
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html', tasks=tasks)

#route - delete an item
@app.route('/delete/<int:id>')
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Error: {e}"
    
#route - edit an item
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id:int):
    edit_task = MyTask.query.get_or_404(id)
    if request.method == 'POST':
        edit_task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error: {e}"
    else:
        return render_template('edit.html', task=edit_task)

#run app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)