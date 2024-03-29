from flask_login import current_user
from wtforms import StringField, validators, PasswordField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from flask_intro.models import User
from flask_wtf.file import FileField, FileAllowed


class RegistratForm(FlaskForm):
    fname = StringField("First Name", validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=20)])
    Email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    Confirm_password = PasswordField("Confirm Password",validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up Now")

    def validate_email(self, Email):
        user = User.query.filter_by(email=Email.data).first()
        if user:
            raise ValidationError('This email has been used before')


class LoginForm(FlaskForm):
    Email = StringField('Email Address', validators=[
        DataRequired(), Email()
    ])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateForm(FlaskForm):
    fname = StringField("First Name", validators=[DataRequired(), Length(min=2, max=20)])

    lname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=20)])

    Email = StringField("Email Address", validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField("Update")

    def validate_email(self, Email):
        if Email.data != current_user.email:
            user = User.query.filter_by(email=Email.data).first()
            if user:
                raise ValidationError('This email has been used before')



class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')