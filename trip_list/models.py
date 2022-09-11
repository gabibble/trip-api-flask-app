#ORM transfers flask class models to pgadmin tables
from flask_sqlalchemy import SQLAlchemy

#sends models to db as tables
from flask_migrate import Migrate

#sets user id
import uuid #sets id for user

from datetime import datetime

#flask security; we can't see password
from werkzeug.security import generate_password_hash, check_password_hash

#create tokens
import secrets 

# importsv from flask_login
from flask_login import UserMixin, LoginManager

#imports for flssk marshmelllow 
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = "")
    last_name = db.Column(db.String(150), nullable = True, default = "")
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(150), nullable = True, default = "")
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default ='', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    ## once you build dron table, comeback and add relationship!
    trip = db.relationship('Trip', backref = "owner", lazy = True)

    def __init__(self, email, first_name = "", last_name = "", id = "", password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.email} has been added!"

#TODO Add trip


class Trip(db.Model):
    id = db.Column(db.String, primary_key = True)
    trip_name = db.Column(db.String(150))
    city = db.Column(db.String(150))
    state = db.Column(db.String(150), nullable = True)
    country = db.Column(db.String(150), nullable = True)
    people = db.Column(db.String(150), nullable = True)
    accommodation = db.Column(db.String(150), nullable = True)
    trip_length = db.Column(db.String(150), nullable = True)
    trip_date = db.Column(db.String(150), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)


    def __init__(self, trip_name, city, state, country, people, accommodation, trip_length, trip_date, user_token, id=""):
        self.id = self.set_id()
        self.trip_name = trip_name
        self.city = city
        self.state = state
        self.country = country
        self.people = people
        self.accommodation = accommodation
        self.trip_length = trip_length
        self.trip_date = trip_date
        self.user_token = user_token

    def __repr__(self):
        return f"The following trip has been added: {self.trip_name}"

    def set_id(self):
        return secrets.token_urlsafe()
#helps data go to insomnia
class TripSchema(ma.Schema):
    class Meta:
        fields = ['id', 'trip_name', 'city', 'state', 'country', 'people', 'accommodation', 'trip_length', 'trip_date']

trip_schema = TripSchema()
trips_schema = TripSchema(many = True)