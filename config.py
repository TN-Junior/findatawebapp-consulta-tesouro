import os
from dotenv import dotenv_values

file = __file__
basedir = os.path.abspath(os.path.dirname(file))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Carregar variáveis do .env
    env_values = dotenv_values(".env")

    # Configurações de e-mail
    MAIL_SERVER = env_values.get('MAIL_SERVER', 'localhost')  # Valor padrão
    MAIL_PORT = int(env_values.get('MAIL_PORT', 25))  # Valor padrão
    MAIL_USE_TLS = env_values.get('MAIL_USE_TLS', 'False').lower() in ['true', '1', 't']
    MAIL_USERNAME = env_values.get('MAIL_USERNAME', None)
    MAIL_PASSWORD = env_values.get('MAIL_PASSWORD', None)
    ADMINS = env_values.get('ADMINS', '').split(',')  # Dividir em lista

