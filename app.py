import logging
from os import path
from datetime import datetime  # Import the datetime module
from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab8.db'  # Specify the database URI
db = SQLAlchemy(app)  # Initialize the SQLAlchemy instance

# Define the database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    height = db.Column(db.Float)  # didn't decide what to put it in yet
    weight = db.Column(db.Float)  # kgs for now
    exercise_data = relationship('ExerciseData', backref='user', lazy=True)
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

# Function to create the database
def create_database():
    dbname = 'lab8.db'
    if not path.exists(dbname):
        with app.app_context():
            db.create_all()
            print('Created Database!')

# Routes
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html', title='Sign Up')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        

    return render_template('login.html', title='Login')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Add logout functionality here
    pass

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/profile', methods=['GET'])
def profile():
    # Add profile retrieval logic here
    return render_template('profile.html', title='Profile')

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    # Add profile update logic here
    pass

@app.route('/settings')
def settings():
    # Add settings retrieval logic here
    return render_template('settings.html', title='Settings')

@app.route('/update_settings', methods=['POST'])
def update_settings():
    # Add settings update logic here
    pass

@app.route('/goals', methods=['GET', 'POST'])
def goals():
    # Add goals logic here
    pass

@app.route('/goals2')
def goals2():
    return render_template('goals2.html', title='Goals')

@app.route('/healthandfitness', methods=['GET', 'POST'])
def data_input():
    # Add health and fitness data input logic here
    pass

@app.route('/workoutplan', methods=['GET', 'POST'])
def workoutplan():
    # Add workout plan logic here
    pass

@app.route('/update_workoutplan')
def update_workoutplan():
    # Add update workout plan logic here
    pass

@app.route('/exercise')
def exercise():
    return render_template('exercise.html', title='Exercise')

if __name__ == '__main__':
    create_database()  # Create the database if it doesn't exist
    app.run(debug=True)
