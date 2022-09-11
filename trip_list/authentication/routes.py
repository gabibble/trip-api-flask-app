from flask import Blueprint, render_template, request, redirect, url_for, flash
#connect userform from forms.py:
from trip_list.forms import UserLoginForm
#connecting to DB (before you instantiate t)
from trip_list.models import User, db, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


# https://flask-wtf.readthedocs.io/en/1.0.x/quickstart/#validating-forms

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == "POST" and form.validate_on_submit():
            #before it works, create form.html, form.py and send bp to innit
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            print(first_name, last_name, email, password)
            # STOP HERE AND DO OTHER STUFF! Check if your form shows up and then 
            # instantiiating user(comment this put until u create user class and DB first! also update .env and init!)
            user = User(email, password = password, first_name = first_name, last_name=last_name)
            db.session.add(user)
            db.session.commit()
            ##
            flash(f"You have created a user account {email}", 'user-created')
            return redirect(url_for('auth.login'))
    except:
        raise Exception('nope!')

    #once you instantiate form, don't forget form = form
    return render_template('signup.html', form = form)



@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = UserLoginForm()
    try:
        print("trying")
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)
            #autenticate user (create user class and db first!!)
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in!', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Your email/password invorrect', 'auth-failed')
                return redirect(url_for('auth.login'))
    except:
        raise Exception('nope!')
    return render_template('login.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))


