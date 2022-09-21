from flask import Blueprint , redirect , flash , session , render_template , request
from multipong.utils import is_authenticated
from multipong.models import Room , User
from multipong.ext import db , socketio
from flask_socketio import join_room , leave_room
from sqlalchemy import or_


rooms = Blueprint("rooms", __name__ , template_folder="templates" , static_folder="static")


@rooms.route("/create_room" , methods = ["POST"])
def create_room():
    if not is_authenticated():
        flash("you need to have an account")
        return redirect("/")

    player1 = User.query.filter_by(_id = session["_id"]).first()
    room = Room(player1=player1)
    db.session.add(room)
    db.session.commit()
    return redirect(f"/room/{room.public_id}")


@rooms.route("/room/<room_id>")
def game_room(room_id):
    room = Room.query.filter_by(public_id = room_id).first()

    if not room or not is_authenticated():
        return redirect("/")


    user = User.query.filter_by(_id = session["_id"]).first()

    p1_count = Room.query.filter_by(player1 = user).count()
    p2_count = Room.query.filter_by(player2 = user).count()
    if room.player1 == user and p1_count != 1:
        return redirect("/")

    if p2_count != 0:
        return redirect("/")

    if room.player1 != user:
        room.player2 = user
        db.session.commit()

    return render_template('room.html', room_url = f"/room/{room.public_id}")



def get_current_room_by_user(user) :
    room = Room.query.filter(or_(Room.player1 == user,Room.player2 == user)).first()
    
    return room

def get_player(user , room):
    if room.player1 == user:
        return "p1"
    if room.player2 == user:
        return "p2"
    return None



@socketio.on("connect", namespace="/room")
def room_connection():
    print("---------------")
    if is_authenticated():
        user = User.query.filter_by(_id = session["_id"]).first()
        room = get_current_room_by_user(user)
        if room:
            
            data = []
            player1 = room.player1
            player2 = room.player2


            if player1:
                data.append({"username" : player1.username, "player" : "player1"})

            if player2:
                data.append({"username" : player2.username, "player" : "player2"})

            join_room(room.public_id)


            socketio.emit("player_data", data , to=room.public_id, namespace ="/room")





@socketio.on("disconnect" , namespace="/room")
def room_disconnect():
    pass





#check if they are authenticated
#check if they are in the room
#check which player they are
#send a response

