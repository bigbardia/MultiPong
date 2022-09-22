from flask import Blueprint , render_template
from multipong.models import PublicChat

views = Blueprint("views" , __name__ , template_folder="templates" , static_folder="static")


@views.route("/")
def index():
    context = {
        "chats" : PublicChat.query.all()[-10:]
    }
    return render_template("index.html" , **context)


@views.route("/pong_test_game")
def pong_test_game():
    return render_template("pong.html")

