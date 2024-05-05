import bcrypt
from flask_wtf import FlaskForm
import logging
from os import path
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, LoginManager, UserMixin, login_user, logout_user
from sqlalchemy import Enum
from flask_bcrypt import Bcrypt
from wtforms import IntegerField, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange



LOGFILE = 'lab8.log'
LOGFORMAT = '%(asctime)s %(levelname)s %(message)s' # Define the log format
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, format=LOGFORMAT) # Configure logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ourdatabase.db'
app.secret_key = 'secretkey'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You need to log in to access this page.'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def create_database():
    """Function that starts the website and shows the current time""" 
    dbname = 'ourdatabase' 
    if not path.exists(dbname):
        with app.app_context():
            db.create_all()
            print('Created Database!')





class User(db.Model, UserMixin):
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



class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    start_date = db.Column(db.DateTime(timezone=True), nullable=False)
    end_date = db.Column(db.DateTime(timezone=True), nullable=False)
    progress = db.Column(db.Integer, nullable=False, default=0)
    goal_type = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Goal(id={self.id}, title={self.title}, description={self.description}, start_date={self.start_date}, end_date={self.end_date}, progress={self.progress}, type={self.goal_type}, user_id={self.user_id})"
    


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Confirm Password"})
    name = StringField(validators=[InputRequired(), Length(max=100)], render_kw={"placeholder": "Name"})
    height = IntegerField(validators=[InputRequired(), NumberRange(min=1)], render_kw={"placeholder": "Height (cm)"})
    weight = IntegerField(validators=[InputRequired(), NumberRange(min=1)], render_kw={"placeholder": "Weight (kg)"})
    age = IntegerField(validators=[InputRequired(), NumberRange(min=1)], render_kw={"placeholder": "Age"})
    submit = SubmitField('registration')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})                  
    submit = SubmitField('login')











@app.route('/')

@app.route('/about')
def about():
    return render_template('about.html',)

@app.route('/contactsean')
def contact_sean():
    return render_template('contactsean.html',)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')




@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', category='success')
        return redirect(url_for('login'))  # Redirect to login page after successful registration
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Logged in successfully.', category='success')
                return redirect(url_for('dashboard'))
    return render_template('login.html',form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        goal_type = request.form.get('type')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
        user_id = current_user.id
        new_goal = Goal(title=title, description=description, goal_type=goal_type,start_date=start_date, end_date=end_date, user_id=user_id)
        db.session.add(new_goal)
        db.session.commit()
        flash('Goal created successfully!', category='success')
        return redirect(url_for('goals'))
    else:
        user_id = current_user.id
        user_goals = Goal.query.filter_by(user_id=user_id).all()
        return render_template('goals.html', goals=user_goals)


@app.route('/displaygoals', methods=['GET', 'POST'])
@login_required
def display_goals():
    user_id = current_user.id
    user_goals = Goal.query.filter_by(user_id=user_id).all()
    return render_template('displaygoals.html', goals=user_goals)


@app.route('/exercise')
def exercise():
    return render_template('exercise.html')

@app.route('/healthandfitness')
def health_and_fitness():
    return render_template('healthandfitness.html')



@app.route('/profile')
def profile():
    if 'username' not in session:
        flash('You need to log in to access this page.', category='error')
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['username']).first()  # Get the current date and time
    return render_template('profile.html', user=user, name=user.name, height=user.height, weight=user.weight, age=user.age, )



@app.route('/update_profile', methods=['POST'])
def update_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        height = request.form.get('height')
        weight = request.form.get('weight')
        age = request.form.get('age')
        user = User.query.filter_by(username=session['username']).first()

        user.name = name
        user.height = height
        user.weight = weight
        user.age = age

        db.session.commit()

        flash('Profile updated successfully', category='success')

        return redirect(url_for('profile'))




@app.route('/workoutplan')
def workout_plan():
    return render_template('workoutplan.html')





if __name__ == '__main__':
    create_database()
    app.run(debug=True)
