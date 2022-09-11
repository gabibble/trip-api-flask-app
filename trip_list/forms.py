#import flask forms! #https://wtforms.readthedocs.io/en/3.0.x/forms/
from flask_wtf import FlaskForm 
#import fields you need for thr form # https://wtforms.readthedocs.io/en/3.0.x/fields/
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
#impirt validators, makes sure email is valid, makes sure #https://wtforms.readthedocs.io/en/3.0.x/validators/
from wtforms.validators import InputRequired, Email

class UserLoginForm(FlaskForm):
    first_name = StringField('First name')
    last_name = StringField('Last name')
    email = StringField('Email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit_button = SubmitField()


class SubmitTrip(FlaskForm):
    trip_name = StringField('Trip Name (i.e. Spring Break trip)', validators = [InputRequired()])
    city = StringField('City', validators = [InputRequired()])
    state = StringField('State/Province')
    country = StringField('Country')
    people = IntegerField('How many people are going?')
    accommodation = StringField('Accommodation Type:')
    trip_length = IntegerField('How many nights are you staying?')
    trip_date = DateField('Trip starting date:')
    submit_button = SubmitField()