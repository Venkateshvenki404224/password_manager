from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
from .models import PassList
import json

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
    if request.method=="POST":
        web = request.form.get('url')
        name = request.form.get('username')
        password = request.form.get('psw')

        if len(name)< 4:
            flash('Enter a valid email id.', category='error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            pass_list = PassList(email=name,website=web,password=password,user_id=current_user.id)
            db.session.add(pass_list)
            db.session.commit()
            flash('Password Added!',category='success')

    return render_template("addpass.html", user=current_user)


@views.route('/')
@login_required
def home():
    return render_template("home.html",user=current_user)

@views.route('/check')
@login_required
def check():
        return render_template("check.html",user=current_user)