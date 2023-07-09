import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from config import Config
from flask import Flask
from flask.helpers import get_root_path
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from dash import Dash
import dash_bootstrap_components as dbc

# sets a database and its migration
db = SQLAlchemy()
migrate = Migrate()
# sets a logging service
login = LoginManager()
# to forces users to login, it needs to know
# what is the view function that handles logins
login.login_view = 'auth.login'
# send emails to users
mail = Mail()
# css framework
bootstrap = Bootstrap()


def create_app(config_class=Config):
    # create a flask instance
    app = Flask(__name__)

    # call configs values from Config class
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.dashboards.monitoramento.layout import layout
    from app.dashboards.monitoramento.calls import callbacks
    register_dash_app(app, 'Monitoramento', 'monitoramento', layout, callbacks)

    from app.dashboards.base_quente.layout import layout
    from app.dashboards.base_quente.calls import callbacks
    register_dash_app(app, 'Base Quente', 'base-quente', layout, callbacks)

    from app.dashboards.capag.layout import layout
    from app.dashboards.capag.calls import callbacks
    register_dash_app(app, 'CAPAG', 'capag', layout, callbacks)

    from app.dashboards.caf.layout import layout
    from app.dashboards.caf.calls import callbacks
    register_dash_app(app, 'CAF', 'caf', layout, callbacks)

    from app.dashboards.stn.layout import layout
    from app.dashboards.stn.chamadas import callbacks
    register_dash_app(app, 'Tesouro Regional', 'stn', layout, callbacks)

    from app.dashboards.central.layout import layout
    from app.dashboards.central.calls import client_calls
    register_dash_app(
        app, 'Central de Previsões', 'central', layout, client_calls
    )

    # the code above creates a SMTPHandler instance to only reports errors
    # and finally attaches it to the app.logger object from Flask
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or \
                    app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'],
                          app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='FinData Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

            # make log files
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/findata.log',
                                               maxBytes=10240,
                                               backupCount=10)
            # includes timestamp, logging level, message and
            # source file and line number from where the log entry originated
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('FinData startup')

    return app


def register_dash_app(app, title, base_pathname, layout, callback_funcs):
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport",
                     "content": "width=device-width, "
                                "initial-scale=1, "
                                "shrink-to-fit=no"}

    my_dash_app = Dash(
        __name__,
        server=app,
        url_base_pathname=f'/dashboards/{base_pathname}/',
        assets_folder=get_root_path(__name__) +
                      f'/dashboards/{base_pathname}/assets/',
        suppress_callback_exceptions=True,
        external_stylesheets=[
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/"
            "css/font-awesome.min.css",
            dbc.themes.LUMEN
        ],
        meta_tags=[meta_viewport]
    )

    with app.app_context():
        my_dash_app.title = title
        my_dash_app.layout = layout
        callback_funcs(my_dash_app)
    _protect_dash_views(my_dash_app)


def _protect_dash_views(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_func] = login_required(
                dash_app.server.view_functions[view_func])


# imports files that uses server
# its stays at bottom to avoid circular imports
from app import models
