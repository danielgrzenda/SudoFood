from flask import render_template, flash, redirect, request, url_for
from application import app, db
from application.forms import LoginForm, RegistrationForm, EditProfileForm, \
    EnterRecipeForm
from flask_login import current_user, login_user, logout_user, login_required
from application.models import User, InputRecipe
from werkzeug.urls import url_parse
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")


@app.route('/user/<username>')
@login_required
def user(username):
    """
    Route to users page
    :param username:
    :return:
    """
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.username == user.username:
        return render_template('user.html', title=current_user.username,
                               user=user)
    return redirect(url_for('profile_unavailable'))


@app.route('/profile_unavailable')
def profile_unavailable():
    return render_template('profile_unavailable.html', title='Unavailable')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route to login page
    :return:
    """
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
    form = LoginForm()
    # this 'if' only gets activated on POST requests
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user', username=current_user.username)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/your_recipes')
@login_required
def your_recipes():
    """
    Route to your_recipes page
    :return:
    """
    recipes = InputRecipe.query.filter_by(user_id=current_user.id)
    return render_template('your_recipes.html', title='Your Recipes',
                           user=current_user, recipes=recipes)


@app.route('/logout')
@login_required
def logout():
    """
    Logs out user
    :return:
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Checks if username/email
    :return:
    """
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.country = form.country.data
        current_user.city = form.city.data
        current_user.date_of_birth = form.date_of_birth.data
        current_user.sex = form.sex.data
        current_user.weight = form.weight.data
        current_user.height = form.height.data
        current_user.workouts_per_week = form.workouts_per_week.data
        current_user.goal = form.goal.data
        current_user.activity_level = form.activity_level.data
        db.session.commit()
        flash('Your changes have been saved!')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.country.data = current_user.country
        form.city.data = current_user.city
        form.date_of_birth.data = current_user.date_of_birth
        form.sex.data = current_user.sex
        form.weight.data = current_user.weight
        form.height.data = current_user.height
        form.workouts_per_week.data = current_user.workouts_per_week
        form.goal.data = current_user.goal
        form.activity_level.data = current_user.activity_level
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/enter_recipe', methods=["GET", "POST"])
@login_required
def enter_recipe():
    form = EnterRecipeForm()
    if form.validate_on_submit():
        recipe = InputRecipe(title=form.title.data,
                             servings=form.servings.data,
                             ingredients=form.ingredients.data,
                             user_id=current_user.id)
        db.session.add(recipe)
        db.session.commit()
        flash('Your recipe was added')
        return redirect(url_for('enter_recipe'))
    return render_template("enter_recipe.html", title="Enter Recipe",
                           form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
