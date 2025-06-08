from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField
from wtforms import validators
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone number', validators=[DataRequired()])
    postal = IntegerField('Postal code', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    street = StringField('Street name and number ', validators=[DataRequired()])
    submit = SubmitField('Register')