from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)

with open('../MachineLearning/picklefiles/recipe_id.pkl','rb') as f:
    recipe_id = pickle.load(f)

with open('../MachineLearning/picklefiles/ingredients.pkl','rb') as f:
    ingredients = pickle.load(f)

with open('../MachineLearning/picklefiles/nutrients.pkl','rb') as f:
    nutrients = pickle.load(f)

with open('../MachineLearning/picklefiles/servings.pkl','rb') as f:
    servings = pickle.load(f)


# avoids the circular imports
from application import routes, models
