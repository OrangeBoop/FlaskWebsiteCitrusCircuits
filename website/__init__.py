from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'boom'

    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}' #Configs Database to the website Folder
    db.init_app(app) #Initialize a Flask application for use with this extension instance.

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix ='/') # All of the URL that is stored inside of this blueprint file are accessed here \
    app.register_blueprint(auth, url_prefix ='/')

    from .models import User, Note
    with app.app_context():
        if not path.exists('website/'+ DB_NAME):
            print("Created Database")
            db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    
    return app

