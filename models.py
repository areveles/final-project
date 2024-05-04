from .import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(54), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    height = db.Column(db.Float)  # didn't decide what to put it in yet
    weight = db.Column(db.Float)  # kgs for now
    exercise_data = relationship('ExerciseData', backref='user', lazy=True)
    workout_plan = relationship('WorkoutPlan',backref='user', lazy=True)
    calorie_intake = db.Column(db.Float)

class ExerciseData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calorie_intake = db.Column(db.Float)
    exercise_type = db.Column(db.String(50))
    num_reps = db.Column(db.Integer)
    num_sets = db.Column(db.Integer)
    calorie_burn = db.Column(db.Float)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class WorkoutPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    num_days = db.Column(db.Integer)
    total_calorie_burn = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)