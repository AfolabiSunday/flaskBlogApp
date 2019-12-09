from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from flask_intro.models import User


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