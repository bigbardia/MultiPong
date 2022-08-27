from flask import (
    Blueprint,
    request,
    session,
    redirect,
    jsonify
)

from multipong.models import User , db
from multipong.ext import socketio
from multipong.utils import get_current_user, is_authenticated


auth = Blueprint("auth" , __name__)

def valid_username(username : str) -> bool:
    VALID = "abcdefghijklmnopqrstuvwxyz"
    VALID += VALID.upper()
    VALID += "1234567890"

    for c in username:
        if not c in VALID:
            return False
    return True

def valid_password(password : str):
    return len(password) > 0


def login_user(user :User):
    session.clear()
    session.permanent = True
    session["_id"] = user._id



@auth.route("/signup" , methods = ["GET" , "POST"])
def signup():

    data = request.get_json(force = True)
    errors = []
    username = data.get("username" ,"")
    password = data.get("password" , "")
    password2 = data.get("password2" , "")

    if len(username) ==  0:
        errors.append("you need a username")

    elif len(username) > 20:
        errors.append("password too large")

    elif not valid_username(username):
        errors.append("invalid characters")

    elif User.query.filter_by(username = username).first():
        errors.append("username already taken")


    if not valid_password(password):
        errors.append("you need a password")

    elif password != password2:
        errors.append("passwords don't match")


    if errors == []:
        user = User(username , password)

        db.session.add(user)
        db.session.commit()

        login_user(user)

        return redirect("/"),301

    return jsonify(errors)

@auth.route("/login" , methods = ["GET","POST"])
def login():

    data = request.get_json(force=True)
    username = data.get("username" , "")
    password = data.get("password" , "")

    user = User.query.filter_by(username = username).first()
    if user:
        if user.verify_password(password):
            login_user(user)
            return redirect("/") , 301
    return jsonify({"error":"failed"})


@auth.route("/logout" , methods = ["GET"])
def logout():
    session.clear()
    session.permanent = True
    return redirect("/")

@auth.route("/get_username")
def get_username():
    if is_authenticated():
        user = get_current_user()
        return user.username
    return ""


@auth.route("/test")
def test():
    return f"{session.items()}"

