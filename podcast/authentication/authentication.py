from flask import Blueprint, render_template, redirect, url_for, session, request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

from functools import wraps
from flask import flash

import podcast.adapters.repository as repo
import podcast.authentication.service as services

authentication_blueprint = Blueprint('authentication_bp', __name__, url_prefix='/authentication')

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_unique = None
    if form.validate_on_submit():
        try:
            services.add_user(repo.repo_instance, form.user_name.data, form.password.data)
            flash('Registration successful!', 'success')  # Flash success message
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            flash('Username already exists! Please choose a different username.', 'error')  # Flash error message
    return render_template('auth.html',
                           title='Register',
                           form=form,
                           user_name_error_message=user_name_unique,
                           handler_url=url_for('authentication_bp.register')), 400


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = services.get_user(repo.repo_instance, form.user_name.data)
            services.authenticate_user(user['username'], form.password.data, repo.repo_instance)
            session.clear()
            session['username'] = user['username']
            flash('Login successful!', 'success')  # Flash a success message for login
            return redirect(url_for('home_bp.home'))

        except services.UnknownUserException:
            flash('Username not recognized - please try again or create an account.', 'error')  # Flash error message

        except services.AuthenticationException:
            flash('Password does not match the given username. Please check and try again.',
                  'error')  # Flash error message

    return render_template('auth.html',
                           title='Login',
                           form=form,
                           is_login=True)  # Add this line


@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    flash('Logout successful!', 'success')  # Flash success message
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view

class PasswordValidate:
    def __init__(self, message = None):
        if not message:
            message = (u'Your password must contain at least 8 characters, an upper case letter, a lower case letter,\
                       and a digit.')
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)

class UsernameValidate:
    def __init__(self, message = None):
        if not message:
            message = (u'Your username must not contain capital letters.')
        self.message = message

    def __call__(self, form, field):
        if not field.data.islower():
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    user_name = StringField('Username:', [
        DataRequired(message='A username is required.'),
        Length(min=3, message='Username is too short. Please enter a username longer than 3 characters.'),
        UsernameValidate()])
    password = PasswordField('Password:', [
        DataRequired(message='A password is required.'),
        PasswordValidate()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Login')