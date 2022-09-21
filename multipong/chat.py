from multipong.ext import socketio , db
from multipong.models import PublicChat
from multipong.utils import is_authenticated, get_current_user, to_datetime

online_users = 0


@socketio.on("connect" , namespace="/")
def chat_connection():
    global online_users
    if is_authenticated():
        user = get_current_user()
        online_users += 1
        socketio.emit("user_joined_chat" , f"{user.username} Connected!" , broadcast = True )
        socketio.emit("online_users" , online_users , broadcast = True)


@socketio.on("disconnect" , namespace="/")
def chat_disconnect():
    global online_users
    if is_authenticated():
        user = get_current_user()
        online_users -= 1
        socketio.emit("user_left_chat" , f"{user.username} Disconnected :(" , broadcast = True)
        socketio.emit("online_users" , online_users , broadcast = True)


@socketio.on("public_chat" , namespace="/")
def broadcast_public_chat(msg):
    if is_authenticated() and len(msg)>0 and msg.count(" ") != len(msg):

        user = get_current_user()
        pc = PublicChat(msg , user)
        db.session.add(pc)
        db.session.commit()
        socketio.emit("public_chat" , {
            "username" : user.username,
            "text"  : msg,
            "date" : to_datetime(pc.timestamp)
        } , broadcast = True)
