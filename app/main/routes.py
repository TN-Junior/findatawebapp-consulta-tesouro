from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
# from app.main.forms import EditProfileForm
from app.models import User
from datetime import datetime
from app.main import bp


@bp.route("/")
@bp.route("/index")
@bp.route("/findata")
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           title="Home",
                           posts=posts)


@bp.route('/user/<username>')
@login_required
def user(username):
    """
    first_or_404() works exactly like first() when there are results,
    but in the case that there are no results automatically sends a 404 error
    :param username:
    :return: user page
    """
    user = User.query.filter_by(username=username).first_or_404()
    # posts = [
    #     {'author': user, 'body': 'Test post #1'},
    #     {'author': user, 'body': 'Test post #2'}
    # ]
    return render_template('user.html', user=user)


@bp.before_app_request
def before_request():
    """
    The @before_request decorator from Flask register the decorated function
    to be executed right before the view function
    :return:
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    return redirect(url_for('main.index'))
    # form = EditProfileForm(current_user.username)
    # if form.validate_on_submit():
    #     current_user.username = form.username.data
    #     current_user.about_me = form.about_me.data
    #     db.session.commit()
    #     flash('Your changes have been saved.')
    #     return redirect(url_for('main.edit_profile'))
    # elif request.method == 'GET':
    #     form.username.data = current_user.username
    #     form.about_me.data = current_user.about_me
    # return render_template('edit_profile.html', title='Edit Profile',
    #                        form=form)
