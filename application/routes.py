from flask import render_template, flash, redirect, request, url_for
from application import app, db
from application.forms import LoginForm, RegistrationForm, EditProfileForm, \
    EnterRecipeForm
from flask_login import current_user, login_user, logout_user, login_required
from application.models import User, InputRecipe
from werkzeug.urls import url_parse
from datetime import datetime
import re
import string
import gensim
from google_images_download import google_images_download

from application import sims_rn, sims, servings, \
    ingredients, nutrients, images, recipe_id, ENGLISH_STOP_WORDS


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")


@app.route('/user/<username>')
@login_required
def user(username):
    """
    Route to users page

    Parameters:
        username (str obj)

    Return:
        url for eithr the user or unavailable profile
    """
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.username == user.username:
        return render_template('user.html', title=current_user.username,
                               user=user,
                               recipes=InputRecipe.query.
                               filter_by(user_id=current_user.id))
    return redirect(url_for('profile_unavailable'))


@app.route('/profile_unavailable')
def profile_unavailable():
    return render_template('profile_unavailable.html', title='Unavailable')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route to login page

    Return:
        If the user's information is saved, sends them to their profile
        If not the user goes to a loginform asking for information to log in
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

    Return:
        the user's saved recipes webpage
    """
    recipes = InputRecipe.query.filter_by(user_id=current_user.id)
    return render_template('your_recipes.html', title='Your Recipes',
                           user=current_user, recipes=recipes)


@app.route('/logout')
@login_required
def logout():
    """
    Logs out user

    Return:
        sends you to index page after logging them out
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Checks if username/email

    Return:
        sends them to register page and has them register then sends them to
        the log in page.
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
    """
    Fills out a form to change your different settings of your profile

    Return:
        Returns them to edit profile page again after filling out info
    """
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
    """
    Enter your recipe you want to search

    Return:
         Enter recipe html page where you input info for a recipe form
    """
    form = EnterRecipeForm()
    if form.validate_on_submit():
        recipe = InputRecipe(title=form.title.data,
                             servings=form.servings.data,
                             ingredients=form.ingredients.data,
                             user_id=current_user.id,
                             picture_url='')
        db.session.add(recipe)
        db.session.commit()

        ten_similar = recommend(recipe.title)

        return render_template("enter_recipe.html", title="Recommended",
                               form=form, similar=ten_similar)

    return render_template("enter_recipe.html", title="Enter Recipe",
                           form=form, similar=None)


def tokeniser(text):
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    text = regex.sub(" ", text.lower())
    words = text.split(" ")
    words = [w for w in words if not len(w) < 2]
    words = [w for w in words if w not in ENGLISH_STOP_WORDS]
    return words


def similarity_object():
    new_rec = [' '.join(x.split('-')[:-1]) for x in recipe_id]
    gen_docs = [[w.lower() for w in tokeniser(text)] for text in new_rec]
    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    tf_idf = gensim.models.TfidfModel(corpus)
    # sim_generator = gensim.similarities.Similarity('MachineLearning/
    # picklefiles/',tf_idf[corpus],num_features=len(dictionary))
    # sim_generator.save('similarity_recipe_name1')
    # sims_rn = gensim.similarities.Similarity.load
    # ('similarity_recipe_name1', mmap=None)
    return dictionary, tf_idf


def recommend(title):
    dictionary, tf_idf = similarity_object()
    query_doc = [w.lower() for w in tokeniser(title)]
    query_doc_bow = dictionary.doc2bow(query_doc)
    query_doc_tf_idf = tf_idf[query_doc_bow]
    sorted_sims = sims_rn[query_doc_tf_idf].argsort()[-5:][::-1]
    rec_recipe = [recipe_id[x] for x in sorted_sims if len(nutrients[x]) != 0]
    new_ing = [ingredients[x] for x in sorted_sims if len(nutrients[x]) != 0]
    new_nutrition = [nutrients[x] for x in sorted_sims if len(nutrients[x])
                     != 0]
    new_servings = [servings[x] for x in sorted_sims if len(nutrients[x])
                    != 0]
    new_img = [images[x] for x in sorted_sims if len(nutrients[x]) != 0]
    z = sorted(range(len([nutrients[x] for x in sorted_sims if
                          len(nutrients[x]) != 0])),
               key=lambda x: [nutrients[y] for y in sorted_sims if
                              len(nutrients[y]) != 0][x][0][2])

    rec_ing = [new_ing[x] for x in z]
    print([(' '.join(rec_recipe[x].split('-')[:-1]), new_nutrition[x][0][2],
            new_servings[x], new_ing[x]) for x in z])
    return [(' '.join(rec_recipe[x].split('-')[:-1]), new_nutrition[x][0][2],
            new_servings[x], new_ing[x], new_img[x]) for x in z]


@app.before_request
def before_request():
    """
    Right before a request is made, checks to see if the user is logged in.
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


def get_image(title):
    response = google_images_download.googleimagesdownload()
    arguments = {'keyword': title, limit: '1'}
