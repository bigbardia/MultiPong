from flask import Blueprint , render_template
from multipong.models import PublicChat, User

views = Blueprint("views" , __name__ , template_folder="templates" , static_folder="static")


@views.route("/")
def index():
    context = {
        "chats" : PublicChat.query.all()[-10:],
        "online_users" : User.query.filter(User.online > 0).count()
    }
    return render_template("index.html" , **context)


@views.route("/pong_test_game")
def pong_test_game():
    return render_template("pong.html")

