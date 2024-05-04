from .import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    notes = db.relationship('Note')