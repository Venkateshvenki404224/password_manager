from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
from .models import PassList
import json
import requests
import hashlib

views = Blueprint('views', __name__)


@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("Notes.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/addpass', methods=['GET', 'POST'])
@login_required
def addpass():
    if request.method == "POST":
        web = request.form.get('url')
        name = request.form.get('username')
        password = request.form.get('psw')
        if len(web) < 2:
            flash('The Name Of The Website Too Short!.', category='error')
        elif len(name) < 4:
            flash('Enter a valid email id.', category='error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            pass_list = PassList(email=name, website=web, password=password, user_id=current_user.id)
            db.session.add(pass_list)
            db.session.commit()
            flash('Password Added!', category='success')
            return render_template("home.html",user=current_user)

    return render_template("addpass.html", user=current_user)


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/check', methods=['GET', 'POST'])
@login_required
def check():
    if request.method == "POST":
        password = request.form.get('password')
        password1 = password.encode()
        sha_password = hashlib.sha1(password1).hexdigest()
        sha_prefix = sha_password[0:5]
        sha_postfix = sha_password[5:].upper()
        url = "https://api.pwnedpasswords.com/range/" + sha_prefix
        payload = {}
        headers = {}
        responce = requests.request("GET", url, headers=headers, data=payload)
        pwnd_dict = {}
        pwnd_list = responce.text.split("\r\n")
        for pwnd_pass in pwnd_list:
            pwnd_hash = pwnd_pass.split(":")
            pwnd_dict[pwnd_hash[0]] = pwnd_hash[1]

        if sha_postfix in pwnd_dict.keys():
            flash(f"Your password have been found {pwnd_dict[sha_postfix]} times", category='error')
        else:
            flash("You password is safe!", category='success')
    return render_template("check.html", user=current_user)


@views.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    name_to_update = PassList.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.website = request.form['website']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("Data Edited", category='success')
            return render_template("home.html", user=current_user, name_to_update=name_to_update)
        except:
            flash("Error!",category='error')
            return render_template('update.html', name_to_update=name_to_update, user=current_user)
    else:
        return render_template("update.html", name_to_update=name_to_update, user=current_user)


@views.route('/delete', methods=['POST'])
@login_required
def delete():
    password = json.loads(request.data)
    passId = password['passId']
    password = PassList.query.get(passId)
    print(password)
    if password:
        if password.user_id == current_user.id:
            db.session.delete(password)
            db.session.commit()

    return jsonify({})


@views.route('/admin', methods=['GET', 'POST'])
@login_required
def delete_user():
    all_data = User.query.all()
    # db.session.delete(all_data)
    # db.session.commit()
    # flash("Deleted User",category='success')
    return render_template("admin.html", user=current_user, users=all_data)


@views.errorhandler(404)
def internal_server_error(e):
    return render_template('404.html'), 404
