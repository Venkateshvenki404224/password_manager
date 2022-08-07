from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from flask_login import login_required, current_user
from .models import Note, User
from . import db
from .models import PassList
import json
import requests
import hashlib
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


views = Blueprint('views', __name__)


@views.route('/add-notes', methods=['GET', 'POST'])
@login_required
def add_notes():
    if request.method == 'POST':
        note1 = request.form.get('note')
        title1 = request.form.get('title')
        print(note1)
        if len(note1) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note1,title=title1,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
            notes = Note.query.order_by(Note.date)
            return render_template("notes.html", notes=notes, user=current_user)
    return render_template("add_note.html", user=current_user)

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    notes = Note.query.order_by(Note.date)
    return render_template("notes.html",notes=notes,user=current_user)


@views.route('/notes/<int:id>',methods=['GET','POST'])
@login_required
def note(id):
    note_id = Note.query.get_or_404(id)
    return render_template('note.html',note_id=note_id,user=current_user)

@views.route('/notes/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_note(id):
    form =  PostForm()
    note_id = Note.query.get_or_404(id)
    if form.validate_on_submit():
        note_id.title = form.title.data
        note_id.data = form.data.data
        db.session.add(note_id)
        db.session.commit()
        flash("Data Updated",category='success')
        return redirect(url_for('views.note',id=note_id.id))
    form.title.data = note_id.title
    form.data.data = note_id.data
    return  render_template('edit_note.html',form=form,user=current_user)


@views.route('/notes/delete/<int:id>',methods=['GET','POST'])
@login_required
def delete_note(id):
    note_id = Note.query.get_or_404(id)
    try:
        db.session.delete(note_id)
        db.session.commit()
        flash("Notes Deleted Succefully",category='success')
        notes = Note.query.order_by(Note.date)
        return render_template("notes.html",notes=notes,user=current_user)
    except:
        flash("Their was an Problem deleting",category='error')
        notes = Note.query.order_by(Note.date)
        return render_template("notes.html", notes=notes, user=current_user)


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
            passlist1 = PassList.query.order_by(PassList.date)
            return render_template("home.html",user=current_user,passlist1=passlist1)
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
def page_not_found(e):
    return render_template('404.html'), 404

# @views.route('/',methods=['GET','POST'])
# def index():
    # return render_template('index.html')

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    data = StringField("Data", validators=[DataRequired()],widget=TextArea())
    submit = SubmitField("Submit")