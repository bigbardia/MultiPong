from flask import Blueprint , redirect , session , render_template
from multipong.utils import is_authenticated
from multipong.models import Room , User
from multipong.ext import db , socketio
from flask_socketio import join_room , leave_room , close_room
from sqlalchemy import or_


rooms = Blueprint("rooms", __name__ , template_folder="templates" , static_folder="static")


@rooms.route("/create_room" , methods = ["POST"])
def create_room():
    if not is_authenticated():
        return redirect("/")


    user = User.query.filter_by(_id = session["_id"]).first()

    room = get_current_room_by_user(user)
    if room:
        return redirect("/")

    room = Room(player1 = user)
    db.session.add(room)
    db.session.commit()
    return redirect(f"/room/{room.public_id}")


@rooms.route("/room/<room_id>")
def game_room(room_id):
    room = Room.query.filter_by(public_id = room_id).first()

    if not room or not is_authenticated():
        return redirect("/")


    user = User.query.filter_by(_id = session["_id"]).first()

    if room.player1 == user:
        if room.active :
            return redirect("/")
        else:
            room.active = True
            db.session.commit()
    else:
        if Room.query.filter_by(player2 = user).count() > 0:
            return redirect("/")
        elif room.player1 != user:
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
    if is_authenticated():
        user = User.query.filter_by(_id = session["_id"]).first()
        room = get_current_room_by_user(user)
        if room:
            player = get_player(user , room)
            if not room.game_started:
                if player == "p1":
                    db.session.delete(room)
                    db.session.commit()
                    socketio.emit("player1_left_before_start" , to = room.public_id , namespace="/room")
                    close_room(room.public_id)

                if player == "p2":
                    leave_room(room.public_id)
                    room.player2 = None
                    db.session.commit()
                    socketio.emit("player2_left_before_start" , to=room.public_id , namespace="/room")

            elif room.game_started:

                room.game_ended = True
                db.session.commit()
                user.score  -= 1
                db.session.commit()
                close_room()
                socketio.emit("player_left" , to= room.public_id , namespace = "/room")



@socketio.on("start_game", namespace="/room")
def start_game():
    if is_authenticated():
        user = User.query.filter_by(_id = session["_id"]).first()
        room = get_current_room_by_user(user)
        if room:
            socketio.emit("start_game" , to=room.public_id)
            room.game_started = True
            db.session.commit()
            socketio.start_background_task(target=game_logic)


def game_logic(room_id):
    p1_score = 0
    p2_score = 0
    while True:
        room = Room.query.filter_by(public_id = room_id).first()
        if room.game_ended:
            break
    
    
    socketio.emit("game_ended" , to=room.public_id , namespace = "/room")
    db.session.delete(room)
    db.session.commit()
    


#check if they are authenticated
#check if they are in the room
#check which player they are
#send a response
