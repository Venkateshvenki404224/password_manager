from flask import Flask, render_template, redirect, session, url_for, request
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)
app.secret_key = "12345678910"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "venki046"
app.config["MYSQL_DB"] = "password_manager"

db = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'email' in request.form and 'psw' in request.form:
            email = request.form['email']
            password = request.form['psw']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE emailid=%s AND password=%s', (email, password))
            info = cursor.fetchone()
            print(info)
            if info is not None:
                if info['emailid'] == email and info['password'] == password:
                    session['succes'] = True
                    return redirect(url_for('profile'))
            else:
                return redirect(url_for('index'))
    return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        if "email" in request.form and "psw" in request.form and 'psw-repeat' in request.form:
            email = request.form['email']
            password = request.form['psw']
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO `password_manager`.`users` (`emailid`, `password`) VALUES (%s,%s);",
                        (email, password))
            db.connection.commit()
            return redirect(url_for('index'))
    return render_template('signup.html')


@app.route('/signup/profile')
def profile():
    if session['succes'] == True:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
