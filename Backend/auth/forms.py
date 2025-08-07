# auth/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo, Length, ValidationError
import re

# Password strength check
def strong_password(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Must contain at least one uppercase letter.')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Must contain at least one lowercase letter.')
    if not re.search(r'\d', password):
        raise ValidationError('Must contain at least one digit.')
    if not re.search(r'[!@#$%^&*]', password):
        raise ValidationError('Must contain at least one special character.')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), strong_password])
    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(), EqualTo('password', message='Passwords must match')])
    role = SelectField('Role', choices=[('user', 'User'), ('worker', 'Worker'), ('admin', 'Admin')],
                       validators=[InputRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In')
