import os
from dotenv import dotenv_values

file = __file__
basedir = os.path.abspath(os.path.dirname(file))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    """
    The configuration variables for email include the server and port, 
    a boolean flag to enable encrypted connections, 
    and optional username and password
    """
    env_values = dotenv_values(".env")

    MAIL_SERVER = env_values['MAIL_SERVER']
    MAIL_PORT = int(env_values['MAIL_PORT'] or 25)
    MAIL_USE_TLS = env_values['MAIL_USE_TLS'] is not None
    MAIL_USERNAME = env_values['MAIL_USERNAME']
    MAIL_PASSWORD = env_values['MAIL_PASSWORD']
    ADMINS = env_values['ADMINS']
