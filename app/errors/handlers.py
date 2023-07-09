from flask import render_template
from app import db
from app.errors import bp

"""
To declare a custom error handler, 
the @errorhandler decorator is used
"""


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """
    To make sure any failed database sessions do not interfere with any
    database accesses triggered by the template, there is a session rollback
    :param error:
    :return: 500 error handling page
    """
    db.session.rollback()
    return render_template('errors/500.html'), 500
