import hashlib
from random import *
import os
from flask import Flask, render_template, redirect, session, url_for, request, flash
from flask_mysqldb import MySQL
import MySQLdb
from function import check,generatescreat

app = Flask(__name__)
app.secret_key = "12345678910"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "venki046"
app.config["MYSQL_DB"] = "password_manager"

db = MySQL(app)

#adding pics
picfolder = os.path.join('static','pics')
app.config['UPLOAD_FOLDER']=picfolder
@app.route('/', methods=['GET', 'POST'])
def index():
    pics1 = os.path.join(app.config['UPLOAD_FOLDER'],'password-manager.jpg')
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
                    flash("Logged in succefully!")
                    return redirect(url_for('profile'))
            else:
                flash("Enter valid email or password")
                return redirect(url_for('index'))
    return render_template("login.html",image = pics1)


@app.route('/signup', methods=['GET', 'POST'])
def new_user():
    pics1 = os.path.join(app.config['UPLOAD_FOLDER'], 'SignUp.png')
    if request.method == 'POST' and "email" in request.form and "psw" in request.form and 'psw-repeat' in request.form:
        email = request.form['email']
        password = request.form['psw']
        repeat_pass = request.form['psw-repeat']
        hashes_pass = hashlib.sha256(password.encode()).hexdigest()
        if password == repeat_pass and check(email) == True and password!="":
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO `password_manager`.`users` (`emailid`, `password`) VALUES (%s,%s);",
                        (email, password))
            cur.execute("INSERT INTO `password_manager`.`screats` (`pass_hash`, `device_secreat`) VALUES (%s,%s);",
                        (hashes_pass, ds))
            db.connection.commit()
            return redirect(url_for('index'))
    return render_template('signup.html')


@app.route('/signup/profile')
def profile():
    if session['succes'] == True:
        return render_template("index.html")

#Creating a device secreat
ds = generatescreat()

if __name__ == '__main__':
    app.run(debug=True)
