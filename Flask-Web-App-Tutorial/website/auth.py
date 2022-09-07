from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from twilio.rest import Client, TwilioException
from .config import account_sid,auth_token,TWILIO_VERIFY_SERVICE_ID

auth = Blueprint('auth', __name__)
sid = account_sid
authtoken = auth_token
service_id = TWILIO_VERIFY_SERVICE_ID
client = Client(sid, authtoken)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                if user.two_factor_enabled():
                    get_otp(user.phone_no)
                    session['username'] = user.email
                    session['phone'] = user.phone_no
                    return redirect(url_for('views.verify_2fa'))
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/', methods=['GET', 'POST'])
def index():
    logout_user()
    return render_template('index.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Enter a valid email id.', category='error')
        elif len(first_name) < 2:
            flash('Enter a valid First Name.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)


def get_otp(phone):
    try:
        verification = client.verify \
            .v2 \
            .services(service_id) \
            .verifications \
            .create(to=phone, channel='sms')
    except TwilioException:
        verification = client.verify \
            .v2 \
            .services(service_id) \
            .verifications \
            .create(to=phone, channel='call')


def check_otp(phone, token):
    try:
        verification_check = client.verify \
            .v2 \
            .services(service_id) \
            .verification_checks \
            .create(to=phone, code=token)
    except TwilioException:
        return False
    return verification_check.status == 'approved'
