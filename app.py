from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

from db_config import get_connection

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)
app.secret_key = "secretkey"

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="dharani",
    database="student_dbms"
)
cursor = db.cursor()

# Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            session['user'] = username
            return redirect('/dashboard')
    return render_template('login.html')


# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')


# Add student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        department = request.form['department']

        cursor.execute(
            "INSERT INTO students (name, age, department) VALUES (%s, %s, %s)",
            (name, age, department)
        )
        db.commit()
        return redirect('/view')

    return render_template('add_student.html')


# View students
@app.route('/view')
def view_student():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template("view_student.html", students=students)

# Update student
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        department = request.form['department']

        cursor.execute(
            "UPDATE students SET name=%s, age=%s, department=%s WHERE id=%s",
            (name, age, department, id)
        )
        db.commit()
        return redirect('/view')

    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    return render_template('update_student.html', student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    db.commit()
    return redirect('/view')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)