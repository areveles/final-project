import extra_functions
from os import path
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
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
            flash('Registration successful', category='success')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
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
    app.run(debug=True)