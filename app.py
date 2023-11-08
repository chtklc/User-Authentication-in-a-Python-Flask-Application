from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import bcrypt
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1495'
app.config['MYSQL_DB'] = 'flaskdb03_userauth'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = os.urandom(24)
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.checkpw(password, user["password"].encode('utf-8')):
            session['name'] = user['name']
            session['email'] = user['email']
            session['isAdmin'] = user['isAdmin']
            return render_template("home.html")
        else:
            return "error password and email not match"
    else:
        return render_template("login.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("home.html")

@app.route('/register/', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hash_password,))
        mysql.connection.commit()
        cur.close()

        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))
    else:
        return render_template("register.html")

@app.route('/admin/', methods=["GET", "POST"])
def admin():
    if 'isAdmin' in session and session['isAdmin'] == 1:
        return render_template('admin.html')
    else:
        return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
