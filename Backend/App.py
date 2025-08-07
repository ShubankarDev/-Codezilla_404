from flask import Flask, render_template, request, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError, Length
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this in production


# Custom validator for strong passwords
def strong_password(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not re.search(r'\d', password):
        raise ValidationError('Password must contain at least one digit.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError('Password must contain at least one special character.')


# Form class
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), strong_password])
    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(), EqualTo('password', message='Passwords must match')])
    role = SelectField('Role', choices=[('user', 'User'), ('worker', 'Worker'), ('admin', 'Admin')],
                       validators=[InputRequired()])
    submit = SubmitField('Sign Up')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        # Simulate saving to DB
        flash(f"Account created for {form.username.data} as {form.role.data}!", "success")
        return redirect(url_for('signup'))

    return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
