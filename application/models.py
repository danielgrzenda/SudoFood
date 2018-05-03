from application import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime


class User(db.Model, UserMixin):
    """
    Class which stores all user information
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    country = db.Column(db.String(40))
    city = db.Column(db.String(40))
    date_of_birth = db.Column(db.DateTime, default=datetime.utcnow)
    sex = db.Column(db.String(1))
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
    workouts_per_week = db.Column(db.Integer)
    goal = db.Column(db.String(2))
    activity_level = db.Column(db.String(2))

    def __repr__(self):
        return '<User %s>' % (self.username)

    def set_password(self, password):
        """
        Generates passwords for user

        Parameter:
            password (str obj)
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if password matches user input

        Parameter:
            password (str obj)

        Return:
            Boolean to see if password hashed is the correct hashed password
        """
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """
        Creates user avatar

        Parameter:
            size (int obj dev set)

        Return:
            returns a hashed image based off a unique email
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/%s?d=identicon&s=%s' \
               % (digest, size)


class InputRecipe(db.Model):
    """
    Stores user input recipe

    Return:
        Recipe saved into database
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(64))
    servings = db.Column(db.Integer)
    ingredients = db.Column(db.Text)
    picture_url = db.Column(db.String(200))

    def __repr__(self):
        return '<Recipe %s>' % (self.title)


@login.user_loader
def load_user(id):
    """
    Loads user querying the database

    Parameter:
        id (str obj)

    Return:
        boolean whether the user is in the database.
    """
    return User.query.get(int(id))
