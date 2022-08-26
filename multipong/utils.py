from flask import session
from multipong.models import User

def is_authenticated()->bool:
    user_id = session.get("_id",None)
    user =User.query.get(user_id)
    if not user_id or not user:
        return False
    return True

def get_current_user():
    user = User.query.get(session["_id"])
    return user
