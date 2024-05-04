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



LOGFILE = 'lab8.log'
LOGFORMAT = '%(asctime)s %(levelname)s %(message)s' # Define the log format
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, format=LOGFORMAT) # Configure logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab8.db'
app.secret_key = 'secretkey'
db = SQLAlchemy(app)

class User(db.Model):
    """Function that starts the website and shows the current time""" 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable = False)
    password = db.Column(db.String(100), nullable = False)


class Note(db.Model):
    """Function that starts the website and shows the current time""" 
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


def create_database():
    """Function that starts the website and shows the current time""" 
    dbname = 'lab8.db'  # Define the database file name
    if not path.exists(dbname):
        with app.app_context():
            db.create_all()
            print('Created Database!')

@app.route('/')
def hello_world():
    """Function that starts the website and shows the current time""" 
    current_time = datetime.now()  # Get the current date and time
    return render_template('mybase.html', current_time=current_time)


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

@app.route('/read')
def read():
    """Function that starts the website"""
    current_time = datetime.now()  # Get the current date and time
    return render_template('read.html',current_time=current_time)



@app.route('/registration', methods=['GET', 'POST'])
def registration():
    """Function that starts the registration page and handles user registration"""

    if request.method == 'POST':
        username = request.form.get('username')  # Access the username stored in the form
        password = request.form.get('password')  # Access the password stored in the form
        cpassword = request.form.get('confirm_password') # Access the cpassword stored in the form
        if len(username) < 6:
            flash('Username must be at least 6 characters long', category='error')
        elif len(password) < 12:
            flash('Password must be at least 12 characters long', category='error')
        elif password != cpassword:
            flash('Passwords do not match', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful', category='success')
            return redirect(url_for('registrationsuccess'))

    current_time = datetime.now()  # Get the current date and time
    return render_template('registration.html', current_time=current_time)


@app.route('/registrationsuccess', methods=['GET', 'POST'])  # Corrected route name here
def registrationsuccess():
    """Function that starts the registration success page"""
    current_time = datetime.now() # Get the current date and time
    return render_template('registrationsuccessful.html',current_time=current_time)



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
            return redirect(url_for('loginsuccessful'))  # Redirect to the login successful page
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


@app.route('/table')
def table():
    """Function that starts the website"""
    current_time = datetime.now() # Get the current date and time
    return render_template('table.html',current_time=current_time)

def loadpasswords():
    """Function that starts the website"""
    commonpasswords = set
    with open('commonpasswords.txt', 'r', encoding='utf-8' ) as passwords:
        for line in passwords:
            commonpasswords.add(line.strip())
    return commonpasswords


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



@app.route('/loginsuccessful', methods=['GET', 'POST'])
def loginsuccessful():
    """Function that starts the login successful page"""
    current_time = datetime.now()  # Get the current date and time
    return render_template('loginsuccessful.html', current_time=current_time)


@app.route('/passwordupdatesuccessful', methods=['GET', 'POST'])
def passwordupdatesuccessful():
    """Function that starts the password update successful page"""
    current_time = datetime.now()  # Get the current date and time
    return render_template('passwordupdatesuccessful.html', current_time=current_time)



if __name__ == '__main__':
    create_database()
    app.run()
    