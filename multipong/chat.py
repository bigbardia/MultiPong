from multipong.ext import socketio , db
from multipong.utils import is_authenticated, get_current_user

@socketio.on("connect")
def chat_connection():
    if is_authenticated():
        user = get_current_user()
        socketio.emit("user_joined_chat" , f"{user.username} Connected!" , broadcast = True )

@socketio.on("disconnect" , namespace="/")
def chat_disconnect():
    print("i am here")
    if is_authenticated():
        user = get_current_user()
        socketio.emit("user_left_chat" , f"{user.username} Disconnected :(" , broadcast = True)

@socketio.on("public_chat")
def broadcast_public_chat(msg):
    if is_authenticated():
        print(msg)
        user = get_current_user()
        socketio.emit("public_chat" , {
            "username" : user.username,
            "text"  : msg,
        } , broadcast = True)
