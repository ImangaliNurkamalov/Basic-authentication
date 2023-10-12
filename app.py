from flask import Flask, request, render_template, session, redirect
import psycopg2
from flask_session import Session
from test import pwd

app = Flask(__name__)

app.secret_key = 'super secret key'
#app.config['SESSION_TYPE'] = 'filesystem'

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
# -------------------------------------- GET METHODS -----------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration')
def register():
    return render_template('registration.html')

@app.route('/user_menu')
def user_menu():
    return render_template('user_menu.html', username = session['username'], password = session['password'])

# ---------------------------------------------------------------------------------------------------------------------

@app.route('/registration', methods=['POST'])
def registration():
    session['username'] = request.form.get('username')
    session['password'] = request.form.get('password')

    conn = psycopg2.connect(host = "localhost", dbname = "first", user = "postgres", password = pwd , port = 5432)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,         
        username VARCHAR(255),
        password VARCHAR(255)       
    );""")
    
    insert_query = """INSERT INTO users(username, password) VALUES (%s, %s);"""
    cur.execute(insert_query, (session['username'], session['password']))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/user_menu")

@app.route('/login', methods = ['POST'])
def login():
    session['username'] = request.form.get('username')
    session['password'] = request.form.get('password')
    conn = psycopg2.connect(host = "localhost", dbname = "first", user = "postgres", password = pwd, port = 5432)
    cur = conn.cursor()
    qry = """SELECT * FROM users WHERE username = %s AND password = %s;"""

    try:
        cur.execute(qry, (session['username'], session['password']))
        rows = cur.fetchall()
        if len(rows) > 0:
            return redirect("/user_menu")
        else:
            return "Invalid username or password"
    except:
        return "Invalid username or password"

if __name__ == '__main__':
    app.run()
