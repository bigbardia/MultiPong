from multipong.ext import socketio , db
from multipong.models import PublicChat
from multipong.utils import is_authenticated, get_current_user

@socketio.on("connect")
def chat_connection():
    if is_authenticated():
        user = get_current_user()
        socketio.emit("user_joined_chat" , f"{user.username} Connected!" , broadcast = True )

@socketio.on("disconnect" , namespace="/")
def chat_disconnect():
    print("i got called * 10")
    if is_authenticated():
        print("i am here" * 10)
        user = get_current_user()
        socketio.emit("user_left_chat" , f"{user.username} Disconnected :(" , broadcast = True)

@socketio.on("public_chat")
def broadcast_public_chat(msg):
    if is_authenticated() and len(msg)>0 and msg.count(" ") != len(msg):

        user = get_current_user()
        pc = PublicChat(msg , user)
        db.session.add(pc)
        db.session.commit()
        socketio.emit("public_chat" , {
            "username" : user.username,
            "text"  : msg,
        } , broadcast = True)
