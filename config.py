import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Configuration class for S3 Database

    Parameters:
        None

    Returns:
        None
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONGODB_DB = 'sudofood_db'
    MONGODB_HOST = '172.31.43.237'
    MONGODB_PORT = '27017'
