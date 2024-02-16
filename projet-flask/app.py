from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL
# import mysql.connector
# from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuration de la base de données MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root' # Utilisateur MySQL
app.config['MYSQL_PASSWORD'] = '' # Mot de passe MySQL
app.config['MYSQL_DB'] = 'todo_list' # Base de données MySQL

mysql = MySQL(app)

# @app.route('/')
# def index():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM tasks")
#     tasks = cur.fetchall()
#     cur.close()
#     return render_template('index.html', tasks=tasks)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/add', methods=['POST'])
# def add():
#     if request.method == 'POST':
#         task = request.form['task']
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
#         mysql.connection.commit()
#         cur.close()
#     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)