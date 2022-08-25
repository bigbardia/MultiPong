from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from flask_socketio import SocketIO

db = SQLAlchemy()
sess = Session()
csrf = CSRFProtect()
socketio = SocketIO()