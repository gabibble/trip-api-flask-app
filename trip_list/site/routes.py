from flask import Blueprint, render_template, request, flash, redirect, url_for
from trip_list.forms import SubmitTrip
from flask_login import current_user
from trip_list.models import Trip, db
# from trip_list.helpers import token_required


site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile', methods = ['GET', 'POST'])
# @token_required
def profile():
    form = SubmitTrip()
    try:
        if request.method == "POST" and form.validate_on_submit():
            #before it works, create form.html, form.py and send bp to innit
            trip_name = form.trip_name.data
            city = form.city.data
            state = form.state.data
            country = form.country.data
            people = form.people.data
            accommodation = form.accommodation.data
            trip_length = form.trip_length.data
            trip_date = form.trip_length.data
            #I think we need token to add a trip? Can't figure out how to get it
            #user_token = current_user_token.token #this is how we added it when adding a trip via api
            user_token = current_user.token #this is how it shows up on profile page. How does 

            print(trip_name, city, state, country, people, accommodation, trip_length, trip_date, user_token)
            # instantiiating trip(comment this put until u create user class and DB first!)
            trip = Trip(trip_name, city, state, country, people, accommodation, trip_length, trip_date , user_token=user_token)
            db.session.add(trip)
            db.session.commit()
            #
            flash(f"Your trip has been added!", 'user-created')
            return redirect(url_for('site.profile'))
    except:
        raise Exception('nope!')
    
    return render_template('profile.html', form = form)