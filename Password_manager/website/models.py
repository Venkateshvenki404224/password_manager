from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=True)
    data = db.Column(db.String(100000000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class PassList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
    phone_no = db.Column(db.String(16), unique=True)
    notes = db.relationship('Note')
    pass_list = db.relationship('PassList')
    # def two_factor_enabled(self):
    #     return self.phone_no is not None
