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
from wtforms import DateField, FloatField, IntegerField, StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange
from flask import jsonify
from sqlalchemy import func
from wtforms import validators

LOGFILE = 'app.log'
LOGFORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, format=LOGFORMAT)

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
    dbname = 'ourdatabase'
    if not path.exists(dbname):
        with app.app_context():
            db.create_all()

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

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exerciseduration = db.Column(db.Integer, nullable=False)
    intensity = db.Column(db.Float, nullable=False)
    caloriesburned = db.Column(db.Integer, nullable=False)
    totalreps = db.Column(db.Integer, nullable=False)
    totalsets = db.Column(db.Integer, nullable=False)
    targetreps = db.Column(db.Integer, nullable=False)
    heartrate = db.Column(db.Integer, nullable=False)
    exercise_type = db.Column(db.String(50), nullable=False)
    completed = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class healthandfitness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    calorie_intake = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    total_calorie_burn = db.Column(db.Integer, nullable=True)
    time_exercised = db.Column(db.Integer, nullable=True)
    average_duration = db.Column(db.Integer, nullable=True)
    average_caloric_burn = db.Column(db.Integer, nullable=True)
    average_caloric_intake = db.Column(db.Integer, nullable=True)
    average_caloric_deficit = db.Column(db.Integer, nullable=True)

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
    
class WorkoutPlanner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer, nullable=False)
    intensity = db.Column(db.Float, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    num_exercises = db.Column(db.Integer, nullable=False)
    workout_date = db.Column(db.DateTime(timezone=True), nullable=False)
    calories_burned = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class WorkoutSession(FlaskForm):
    duration = IntegerField('Duration (in minutes):', validators=[InputRequired(), NumberRange(min=1)])
    intensity = FloatField('Intensity (out of 10):', validators=[InputRequired(), NumberRange(min=0, max=10)])
    frequency = IntegerField('Frequency (times per week):', validators=[InputRequired(), NumberRange(min=1)])
    num_exercises = IntegerField('Number of Exercises:', validators=[InputRequired(), NumberRange(min=1)])
    workout_date = DateField('Workout Date:', validators=[InputRequired()])
    calories_burned = IntegerField('Calories Burned:', validators=[InputRequired(), NumberRange(min=1)])

class WorkoutForm(FlaskForm):
    duration = IntegerField('Duration (in minutes):', validators=[InputRequired(), NumberRange(min=1)])
    intensity = FloatField('Intensity (out of 10):', validators=[InputRequired(), NumberRange(min=0, max=10)])
    frequency = IntegerField('Frequency (times per week):', validators=[InputRequired(), NumberRange(min=1)])
    num_exercises = IntegerField('Number of Exercises:', validators=[InputRequired(), NumberRange(min=1)])
    workout_date = DateField('Workout Date:', validators=[InputRequired()])

    def validate_workout_date(self, workout_date):
        if workout_date.data < datetime.now().date():
            raise ValidationError('Workout date must be in the future.')

    calories_burned = IntegerField('Calories Burned:', validators=[InputRequired(), NumberRange(min=1)])

    def validate_frequency(self, frequency):
        if frequency.data > 7:
            raise ValidationError('Frequency cannot be more than 7 times per week.')

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=12, max=20)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(validators=[InputRequired(), Length(min=12, max=20)], render_kw={"placeholder": "Confirm Password"})
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

class ExerciseForm(FlaskForm):
    exerciseduration = IntegerField('Duration of Exercise (in minutes):', validators=[InputRequired(), NumberRange(min=1)])
    intensity = FloatField('Intensity (out of 10):', validators=[InputRequired(), NumberRange(min=0, max=10)])
    caloriesburned = IntegerField('Calories Burned:', validators=[InputRequired(), NumberRange(min=1)])
    totalreps = IntegerField('Total Reps:', validators=[InputRequired(), NumberRange(min=1)])
    totalsets = IntegerField('Total Sets:', validators=[InputRequired(), NumberRange(min=1)])
    targetreps = IntegerField('Target Reps:', validators=[InputRequired(), NumberRange(min=1)])
    heartrate = IntegerField('Heart Rate:', validators=[InputRequired(), NumberRange(min=1)])
    exercise_type = SelectField('Type of Exercise:', choices=[
        ('PUSHUPS', 'Pushups'),
        ('SITUPS', 'Situps'),
        ('SQUATS', 'Squats'),
        ('LUNGES', 'Lunges'),
        ('PLANKS', 'Planks'),
        ('JUMPING_JACKS', 'Jumping Jacks'),
        ('PULLUPS', 'Pullups'),
        ('BURPEES', 'Burpees'),
        ('MOUNTAIN_CLIMBERS', 'Mountain Climbers'),
        ('CRUNCHES', 'Crunches'),
        ('LEG_RAISES', 'Leg Raises'),
        ('RUN_5K', '5K Run'),
        ('RUN_10K', '10K Run'),
        ('RUN_1MILE', '1 Mile Run'),
        ('BIKE_5MILES', '5 Mile Bike Ride'),
        ('SPRINT_100M', '100m Sprint'),
        ('SWIM_500M', '500m Swim')
    ])
    completed = FloatField('Percentage Completed:', validators=[InputRequired(), NumberRange(min=0, max=100)])

@app.route('/')

@app.route('/about')
def about():
    return render_template('about.html',)

@app.route('/contact')
def contact():
    return render_template('contact.html',)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password, name=form.name.data, height=form.height.data, weight=form.weight.data, age=form.age.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', category='success')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                session['authenticated'] = True
                flash('Logged in successfully.', category='success')
                return redirect(url_for('profile'))
            else:
                flash('Invalid username or password.', category='error')
        else:
            flash('Invalid username or password.', category='error')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.pop('authenticated', None)
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

@app.route('/healthandfitness')
def health_and_fitness():
    return render_template('healthandfitness.html')

@app.route('/save_calorie_intake', methods=['POST'])
@login_required
def save_calorie_intake():
    if request.method == 'POST':
        calorie_intake = int(request.form.get('calories'))
        user_id = current_user.id
        date = datetime.now()
        print(current_user.height, current_user.weight)
        height_meters = current_user.height / 100
        weight_kg = current_user.weight
        bmi = weight_kg / (height_meters ** 2)   
        new_calorie_intake = healthandfitness(
            calorie_intake=calorie_intake,
            user_id=user_id,
            date=date,
            average_caloric_intake=calorie_intake,
            average_caloric_deficit=bmi
        )
        db.session.add(new_calorie_intake)
        db.session.commit()
        
        total_calories = healthandfitness.query.with_entities(func.sum(healthandfitness.calorie_intake)).filter_by(date=date).first()[0]
        
        flash(f"On {date.strftime('%Y-%m-%d')}, you took in {calorie_intake} calories. Total: {total_calories} calories. Average Calorie Intake: {calorie_intake:.2f} calories. Your BMI is {bmi:.2f}.", category='success')
        
        return redirect(url_for('health_and_fitness'))
    else:
        return redirect(url_for('health_and_fitness'))

@app.route('/profile')
@login_required
def profile():
    user = current_user
    return render_template('profile.html', user=user)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        height = request.form.get('height')
        weight = request.form.get('weight')
        age = request.form.get('age')

        user = current_user
        current_user.name = name
        user.height = height
        user.weight = weight
        user.age = age

        db.session.commit()

        flash('Profile updated successfully', category='success')

        return redirect(url_for('profile'))

@app.route('/workoutplanner', methods=['GET', 'POST'])
@login_required
def workout_planner():
    form = WorkoutForm()
    if form.validate_on_submit():
        duration = form.duration.data
        intensity = form.intensity.data
        frequency = form.frequency.data
        num_exercises = form.num_exercises.data
        workout_date = form.workout_date.data
        calories_burned = form.calories_burned.data
        new_workout = WorkoutPlanner(
            duration=duration,
            intensity=intensity,
            frequency=frequency,
            num_exercises=num_exercises,
            workout_date=workout_date,
            calories_burned=calories_burned,
            user_id=current_user.id
        )
        db.session.add(new_workout)
        db.session.commit()

        flash('Workout planner created successfully!', category='success')
        return redirect(url_for('workout_planner'))

    return render_template('workoutplanner.html', form=form)

@app.route('/displayworkouts', methods=['GET'])
@login_required
def displayworkouts():
    user_id = current_user.id
    workouts = WorkoutPlanner.query.filter_by(user_id=user_id).all()
    return render_template('displayworkouts.html', workouts=workouts)

@app.route('/exercise')
@login_required
def exercise():
    form = ExerciseForm()
    return render_template('exercise.html', form=form)

@app.route('/submit_exercise', methods=['POST'])
@login_required
def submit_exercise():
    if request.method == 'POST':
        form = ExerciseForm(request.form)
        if form.validate():
            exerciseduration = form.exerciseduration.data
            intensity = form.intensity.data
            caloriesburned = form.caloriesburned.data
            totalreps = form.totalreps.data
            totalsets = form.totalsets.data
            targetreps = form.targetreps.data
            heartrate = form.heartrate.data
            exercise_type = form.exercise_type.data
            completed = form.completed.data

            new_exercise = Exercise(
                exerciseduration=exerciseduration,
                intensity=intensity,
                caloriesburned=caloriesburned,
                totalreps=totalreps,
                totalsets=totalsets,
                targetreps=targetreps,
                heartrate=heartrate,
                exercise_type=exercise_type,
                completed=completed,
                user_id=current_user.id
            )
            db.session.add(new_exercise)
            db.session.commit()
            flash('Exercise data submitted successfully!', category='success')
            return redirect(url_for('exercise'))
        else:
            flash('Failed to submit exercise data. Please check the form.', category='error')
            return redirect(url_for('exercise'))
    else:
        flash('Method not allowed.', category='error')
        return redirect(url_for('exercise'))

@app.route('/displayexercises', methods=['GET'])
@login_required
def displayexercise():
    user_id = current_user.id
    exercises = Exercise.query.filter_by(user_id=user_id).all()
    return render_template('displayexercises.html', exercises=exercises)

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
