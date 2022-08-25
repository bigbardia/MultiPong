from flask import Blueprint , render_template

views = Blueprint("views" , __name__ , template_folder="templates" , static_folder="static")


@views.route("/")
def index():
    return render_template("index.html")

