from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user, login_user
from .auth import get_otp, check_otp
from .models import Note, User
from . import db
from .models import PassList
import requests
import hashlib
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import TextArea
from twilio.rest import Client
import phonenumbers

views = Blueprint('views', __name__)


# Adding Notes

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
            new_note = Note(data=note1, title=title1, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
            notes = Note.query.order_by(Note.date)
            return render_template("notes.html", notes=notes, user=current_user)
    return render_template("add_note.html", user=current_user)


# Displaying the notes

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    notes = Note.query.order_by(Note.date)
    return render_template("notes.html", notes=notes, user=current_user)


# Displaying Single Notes in a page

@views.route('/notes/<int:id>', methods=['GET', 'POST'])
@login_required
def note(id):
    note_id = Note.query.get_or_404(id)
    return render_template('note.html', note_id=note_id, user=current_user)


# Editing the Notes

@views.route('/notes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    form = PostForm()
    note_id = Note.query.get_or_404(id)
    if form.validate_on_submit():
        note_id.title = form.title.data
        note_id.data = form.data.data
        db.session.add(note_id)
        db.session.commit()
        flash("Data Updated", category='success')
        return redirect(url_for('views.note', id=note_id.id))
    form.title.data = note_id.title
    form.data.data = note_id.data
    return render_template('edit_note.html', form=form, user=current_user)


# Deleting the Notes

@views.route('/notes/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_note(id):
    note_id = Note.query.get_or_404(id)
    try:
        db.session.delete(note_id)
        db.session.commit()
        flash("Notes Deleted Succefully", category='success')
        notes = Note.query.order_by(Note.date)
        return render_template("notes.html", notes=notes, user=current_user)
    except:
        flash("Their was an Problem deleting", category='error')
        notes = Note.query.order_by(Note.date)
        return render_template("notes.html", notes=notes, user=current_user)


# Adding Password

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
            return redirect(url_for('views.password'))
    return render_template("addpass.html", user=current_user)


# Displaying the Passwords

@views.route('/password')
@login_required
def password():
    Password = PassList.query.order_by(PassList.date)
    return render_template("password.html", user=current_user, Password=Password)


# Updating the Passwords

@views.route('/password/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    name_to_update = PassList.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.website = request.form['website']
        name_to_update.email = request.form['email']
        name_to_update.password = request.form['password']
        try:
            # db.session.add(name_to_update)
            db.session.commit()
            flash("Data Edited", category='success')
            return redirect(url_for('views.password'))
        except:
            flash("Error!", category='error')
            return render_template('update.html', name_to_update=name_to_update, user=current_user)
    else:
        return render_template("update.html", name_to_update=name_to_update, user=current_user)


# Deleting PassWords

@views.route('/password/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_password(id):
    password_id = PassList.query.get_or_404(id)
    try:
        db.session.delete(password_id)
        db.session.commit()
        flash("Password Deleted Succefully", category='success')
        Password = PassList.query.order_by(PassList.date)
        return redirect(url_for('views.password'))
    except:
        flash("Their was an Problem deleting", category='error')
        Password = PassList.query.order_by(PassList.date)
        return redirect(url_for('views.password'))


# Checking the Passwords

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
        response = requests.request("GET", url, headers=headers, data=payload)
        pwnd_list = response.text.split("\r\n")

        for pwnd_pass in pwnd_list:
            pwnd_hash = pwnd_pass.split(":")
            if len(pwnd_hash) >= 2:
                if sha_postfix == pwnd_hash[0]:
                    count = pwnd_hash[1]
                    flash(f"Your password has been found {count} times", category='error')
                    return redirect(url_for('views.check'))
        
        flash("Your password is safe!", category='success')

    return render_template("check.html", user=current_user)



# @views.route('/delete', methods=['POST'])
# @login_required
# def delete():
#     password = json.loads(request.data)
#     passId = password['passId']
#     password = PassList.query.get(passId)
#     print(password)
#     if password:
#         if password.user_id == current_user.id:
#             db.session.delete(password)
#             db.session.commit()
#
#     return jsonify({})


@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    all_data = User.query.all()
    # db.session.delete(all_data)
    # db.session.commit()
    # flash("Deleted User",category='success')
    return render_template("index.html", user=current_user, users=all_data)


@views.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@views.route('/home')
@login_required
def home():
    all_data = User.query.all()
    return render_template("home.html", user=current_user, users=all_data)


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    data = StringField("Data", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")


class Enable2faForm(FlaskForm):
    verification_phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Enable 2FA')

    def validate_verification_phone(self, verification_phone):
        try:
            p = phonenumbers.parse(verification_phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            flash("Invalid Phone Number!", category='error')


@views.route('/enable_2fa', methods=['GET', 'POST'])
@login_required
def enable_2fa():
    form = Enable2faForm()
    if form.validate_on_submit():
        session['phone'] = form.verification_phone.data
        get_otp(session['phone'])
        return redirect(url_for('views.verify_2fa'))
    return render_template('enable2fa.html', form=form,user=current_user)


class Confirm2faForm(FlaskForm):
    token = StringField('Token')
    submit = SubmitField('Verify')

@views.route('/verify_2fa', methods=['GET', 'POST'])
def verify_2fa():
    form = Confirm2faForm()
    if form.validate_on_submit():
        phone = session['phone']
        if check_otp(phone, form.token.data):
            del session['phone']
            if current_user.is_authenticated:
                current_user.phone_no = phone
                db.session.commit()
                flash('Two-factor authentication is now enabled')
                return redirect(url_for('views.home'))
            else:
                username = session['username']
                del session['username']
                user = User.query.filter_by(email=username).first()
                login_user(user,remember=True)
                return render_template('home.html',user=current_user)
        flash("Invalid OTP",category='error')
    return render_template('verify_2fa.html', form=form,user=current_user)



class Disable2faForm(FlaskForm):
    submit = SubmitField('Disable 2FA')
    
from flask_login import current_user, login_required

class Disable2faForm(FlaskForm):
    submit = SubmitField('Disable 2FA')

@views.route('/disable_2fa', methods=['GET', 'POST'])
@login_required
def disable_2fa():
    form = Disable2faForm()
    if form.validate_on_submit():
        current_user.phone_no = None
        db.session.commit()
        flash('Two-factor authentication has been disabled', category='success')
        return redirect(url_for('views.home'))
    return render_template('home.html', form=form, user=current_user)

