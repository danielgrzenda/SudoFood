from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    DateField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, \
    Length
from application.models import User


class LoginForm(FlaskForm):
    """
    Stores login data from user input
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """
    Stores registration data from user input
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('That username is taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                'That email is already associatd with a registered account.')


class EditProfileForm(FlaskForm):
    """
    Allows users to edit personal information and stores new input
    """
    country = StringField('Country')
    city = StringField('City')
    date_of_birth = DateField('Date Of Birth')
    weight = IntegerField('Weight')
    height = IntegerField('Height')
    workouts_per_week = IntegerField('Workouts Per Week')
    goal = SelectField('Goals', choices=[('LW', 'Lose Weight'),
                                         ('MW', 'Maintain Weight'),
                                         ('GW', 'Gain Weight')])
    sex = SelectField('Sex', choices=[('M', 'Male'), ('F', 'Female')])
    activity_level = SelectField('Activity Level', choices=[('S', 'Sedentary'),
                                                            ('LA',
                                                             'Lightly Active'),
                                                            ('A', 'Active'), (
                                                            'VA',
                                                            'Very Active')])
    submit = SubmitField('Edit Profile')


class EnterRecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    servings = IntegerField('Servings', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients',
                                validators=[Length(min=0, max=10000)])
    submit = SubmitField('Find Healtheir Versions')
