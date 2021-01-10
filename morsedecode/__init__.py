from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# app initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'flask-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///morsedecode.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db initialization
db = SQLAlchemy(app)
db.init_app(app)


@app.before_first_request
def create_db():
    db.create_all()


# Flask migrate app and db
migrate = Migrate(app=app, db=db)


# Login Manager Flask
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


from morsedecode import routers, models

@login_manager.user_loader
def load_user(user_id):
    if user_id :
        return models.User.query.get(user_id)
