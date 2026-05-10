from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100))
    description = db.Column(db.String(200))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100))
    status = db.Column(db.String(50))

@app.route('/')
def home():

    total_users = User.query.count()
    total_projects = Project.query.count()
    total_tasks = Task.query.count()

    return render_template(
        'dashboard.html',
        total_users=total_users,
        total_projects=total_projects,
        total_tasks=total_tasks
    )

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:
            return render_template('dashboard.html')

        else:
            return "Invalid Email or Password"

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return "User Registered Successfully 🔥"

    return render_template('register.html')
@app.route('/projects', methods=['GET', 'POST'])
def projects():

    if request.method == 'POST':

        project_name = request.form['project_name']
        description = request.form['description']

        new_project = Project(
            project_name=project_name,
            description=description
        )

        db.session.add(new_project)
        db.session.commit()

        return "Project Created Successfully 🔥"

    return render_template('projects.html')
@app.route('/tasks', methods=['GET', 'POST'])
def tasks():

    if request.method == 'POST':

        task_name = request.form['task_name']
        status = request.form['status']

        new_task = Task(
            task_name=task_name,
            status=status
        )

        db.session.add(new_task)
        db.session.commit()

        return "Task Created Successfully 🔥"

    return render_template('tasks.html')
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
