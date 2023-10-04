from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, validators
from wtforms.validators import DataRequired, Email
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    goals = db.relationship('Goal', back_populates='user')


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    completion_percentage = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', back_populates='goals')


with app.app_context():
    inspector = inspect(db.engine)
    if not inspector.has_table('user'):
        db.create_all()


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class GoalForm(FlaskForm):
    description = StringField('Goal Description', validators=[validators.DataRequired()])
    completion_percentage = IntegerField('Completion Percentage', validators=[
        validators.DataRequired(),
        validators.NumberRange(min=0, max=100, message='Completion percentage must be between 0 and 100.')
    ])


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('This email address is already registered. Please use a different email address.', 'danger')
            return redirect(url_for('register'))

        new_user = User(name=name, surname=surname, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route("/", methods=['GET', 'POST'])
def index():
    if 'user_id' in session:
        form = GoalForm(request.form)
        if form.validate_on_submit():
            description = form.description.data
            completion_percentage = form.completion_percentage.data

            user = User.query.get(session['user_id'])
            if user:
                goal = Goal(description=description, completion_percentage=completion_percentage, user=user)
                db.session.add(goal)
                db.session.commit()

                flash('Goal created successfully!', 'success')
                return redirect(url_for('index'))
        user = User.query.get(session['user_id'])

        return render_template("index_logged_in.html", form=form, user=user)
    else:
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()

            if user and user.password == password:
                flash('Login successful!', 'success')
                session['user_id'] = user.id
                return redirect(url_for('index'))
            else:
                flash('Login failed. Please check your credentials and try again.', 'danger')

        return render_template("index.html", form=form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route("/<goal>/<int:days>")
def goals(goal, days):
    return render_template("goals_tracker.html", goal=goal, days=days)


if __name__ == "__main__":
    app.run(debug=True)
