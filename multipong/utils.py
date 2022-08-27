from flask import session
from multipong.models import User
from datetime import datetime
import pytz

def is_authenticated()->bool:
    user_id = session.get("_id",None)
    user =User.query.get(user_id)
    if not user_id or not user:
        return False
    return True

def get_current_user():
    user = User.query.get(session["_id"])
    return user


def to_datetime(timestamp : int):
    dt = datetime.fromtimestamp(timestamp , pytz.timezone("Asia/Tehran"))
    return dt.strftime("%A, %Y-%m-%d %H:%M:%S")
