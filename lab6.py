"""This program makes websites"""
# Sean Grantham
# 10/9/2023
# SDEV 300 6383
# Program that makes websites
# Lab 8


import logging
from os import path
from datetime import datetime  # Import the datetime module
from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, LoginManager, UserMixin, login_user, logout_user


LOGFILE = 'lab8.log'
LOGFORMAT = '%(asctime)s %(levelname)s %(message)s' # Define the log format
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, format=LOGFORMAT) # Configure logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ourdatabase.db'
app.secret_key = 'secretkey'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You need to log in to access this page.'






class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    height = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    notes = db.relationship('Note', backref='user', lazy=True)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_database():
    """Function that starts the website and shows the current time""" 
    dbname = 'ourdatabase'  # Define the database file name
    if not path.exists(dbname):
        with app.app_context():
            db.create_all()
            print('Created Database!')




@app.route('/')

@app.route('/about')
def about():
    """Function that starts the website""" 
    current_time = datetime.now()  # Get the current date and time
    return render_template('about.html',current_time=current_time)

@app.route('/contactsean')
def contact_sean():
    """Function that starts the website"""
    current_time = datetime.now()  # Get the current date and time
    return render_template('contactsean.html',current_time=current_time)




@app.route('/registration', methods=['GET', 'POST'])
def registration():
    """Function that starts the registration page and handles user registration"""

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        cpassword = request.form.get('confirm_password')
        name = request.form.get('name')  # Get the name from the form
        height = request.form.get('height')  # Get the height from the form
        weight = request.form.get('weight')  # Get the weight from the form
        age = request.form.get('age')  # Get the age from the form

        if len(username) < 6:
            flash('Username must be at least 6 characters long', category='error')
        elif len(password) < 12:
            flash('Password must be at least 12 characters long', category='error')
        elif password != cpassword:
            flash('Passwords do not match', category='error')
        else:
            # Create a new user object with the provided information
            new_user = User(username=username, 
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            name=name,
            height=height,
            weight=weight,
            age=age)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful', category='success')
            return redirect(url_for('login'))

    current_time = datetime.now()  # Get the current date and time
    return render_template('registration.html', current_time=current_time)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Function that starts the website"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if a user with the provided username exists
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password, password):
            # Set the session variable to indicate that the user is logged in
            session['username'] = username
            flash('Login successful', category='success')
            return redirect(url_for('profile'))  # Redirect to the login successful page
        log_failed_login_attempt(username)  # Pass the username to the log function

        flash('Invalid username or password', category='error')

    current_time = datetime.now()  # Get the current date and time
    return render_template('login.html', current_time=current_time)

def log_failed_login_attempt(username):
    """Function that starts the website"""
    log_data = {
        'ip': request.remote_addr,
    }
    log_message = f'Failed login attempt for username "{username}"'
    logging.error(log_message, extra=log_data)





@app.route('/passwordupdate', methods=['GET', 'POST'])
def passwordupdate():
    """Function that starts the website"""
    # Step 1: Load common passwords
    def load_passwords():
        common_passwords = set()
        with open('commonpasswords.txt', 'r', encoding='utf-8' ) as passwords:
            for line in passwords:
                common_passwords.add(line.strip())
        return common_passwords

    if request.method == 'POST':
        # Check if the user is logged in (you may use Flask-Login or session management)
        if 'username' not in session:
            flash('You need to log in to update your password.', category='error')
            return redirect(url_for('login'))

        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Verify old password (you need to compare it with the hashed password in the database)
        user = User.query.filter_by(username=session['username']).first()
        if not user or not check_password_hash(user.password, old_password):
            flash('Incorrect old password.', category='error')
        elif len(new_password) < 12:
            flash('Password must be at least 12 characters long.', category='error')
        else:
            # Step 2: Check if the new password is a common password
            common_passwords = load_passwords()
            if new_password in common_passwords:
                flash('Common password detected. Please choose a different password.', category='error')
            else:
                # Check if the new passwords match
                if new_password != confirm_password:
                    flash('New passwords do not match.', category='error')
                else:
                    # Update the user's password in the database
                    user.password = generate_password_hash(new_password, method='sha256')
                    db.session.commit()
                    flash('Password updated successfully.', category='success')
                    return redirect(url_for('passwordupdatesuccessful'))

    current_time = datetime.now()  # Get the current date and time
    return render_template('passwordupdate.html', current_time=current_time)




@app.route('/exercise')
def exercise():
    return render_template('exercise.html')

@app.route('/healthandfitness')
def health_and_fitness():
    return render_template('healthandfitness.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# Profile update route
@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        # Update the user's profile information
        current_user.name = request.form.get('name')
        current_user.height = request.form.get('height')
        current_user.weight = request.form.get('weight')
        current_user.age = request.form.get('age')
        db.session.commit()
        flash('Profile updated successfully', category='success')
        return redirect(url_for('profile'))
    
    return render_template('update_profile.html')



@app.route('/workoutplan')
def workout_plan():
    return render_template('workoutplan.html')




if __name__ == '__main__':
    create_database()
    app.run()
