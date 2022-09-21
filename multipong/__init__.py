from flask import Flask
from dotenv import load_dotenv
import os
from multipong.auth import auth
from multipong.views import views
from multipong.room import rooms
from multipong.ext import db , sess , csrf , socketio
from multipong.utils import is_authenticated , to_datetime


load_dotenv()


def create_app():

    app = Flask(__name__ , template_folder="templates" , static_folder="static")
    app.secret_key = os.environ.get("secret_key")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:{os.environ.get('mysql_password')}@localhost/pongdb"



    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SESSION_TYPE"] = "sqlalchemy"
    app.config["PERMANENT_SESSION_LIFETIME"] = 2 * 7 * 24  * 60 * 60 # 2 weeks
    app.config["SESSION_SQLALCHEMY"] = db


    app.register_blueprint(auth)
    app.register_blueprint(views)
    app.register_blueprint(rooms)


    db.init_app(app)
    sess.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app)
    from multipong import chat

    app.jinja_env.globals.update(is_authenticated = is_authenticated)
    app.jinja_env.globals.update(to_datetime = to_datetime)

    with app.app_context():
        db.create_all()
    
    return app , socketio


