import extra_functions
from os import path
from datetime import datetime, timedelta
from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab8.db'  # Specify the database URI
db = SQLAlchemy(app)  # Initialize the SQLAlchemy instance
app.permanent_session_lifetime = timedelta(minutes=15)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')  
        password = request.form.get('password') 
        cpassword = request.form.get('confirm_password') 
        age = request.form.get('age') 
        height = request.form.get('height')
        weight = request.form.get('weight')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        if not(username and password and cpassword and age and height and weight and first_name and last_name):
            flash('Please ensure all fields are filled out.', category='error')
        elif (len(username) < 4) or (len(username) > 12):
            flash('Username must be between 4 and 12 characters long.', category='error')
        elif not(extra_functions.password_valid(password)):
            flash('Password must be at least 12 characters long, containing one capital letter, one lowercase letter, one number, and one valid special character.', category='error')
        elif ((int(age) < 18) or (int(age) > 125)):
            flash('User age must be at least 18 years old, and no older than 125 years old.')
        elif password != cpassword:
            flash('Passwords do not match.', category='error')
        else:
            flash('Registration successful.', category='success')
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