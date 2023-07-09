from app import create_app, db
from app.models import User, Post

server = create_app()


@server.shell_context_processor
def make_shell_context():
    """
    creates a 'flask shell' context that adds the database
    instance and models to the shell session
    """
    return {'db': db, 'User': User, 'Post': Post}
