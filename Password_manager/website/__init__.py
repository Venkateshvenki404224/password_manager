from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy(app=None)

DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    db.app = app

    app.config['SECRET_KEY'] = 'hjshjhdjahkjshkjdhjsmyverystrongpassword'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Initialize the SQLAlchemy extension with the Flask application
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, PassList

    with app.app_context():
        create_database()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database():
    if not path.exists('website/' + DB_NAME):
        with db.app.app_context():
            db.create_all()
        print('Created Database!')
