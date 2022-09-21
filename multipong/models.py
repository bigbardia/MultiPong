from multipong.ext import db
from passlib.hash import bcrypt
from time import time
from uuid import uuid4


def gen_timestamp():
    return int(time())

def gen_uuid():
    return uuid4().hex

class PublicChat(db.Model):

    _id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text , nullable = False)
    timestamp = db.Column(db.Integer, nullable= False , default = gen_timestamp)
    user_id = db.Column(db.Integer , db.ForeignKey("user._id"))

    def __init__(self ,text , user):
        self.text = text
        self.user = user

    def __repr__(self):
        return self.text    


class Room(db.Model):

    _id = db.Column(db.Integer , primary_key = True)
    public_id = db.Column(db.Text, default = gen_uuid)
    player1_id = db.Column(db.Integer , db.ForeignKey("user._id"))
    player2_id = db.Column(db.Integer , db.ForeignKey("user._id") , nullable = True)


    def __init__(self, player1):
        self.player1 = player1

    def __repr__(self):
        return self.public_id

    def get_url(self):
        return f"/room/{self.public_id}"




class User(db.Model):

    _id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(20) , unique = True)
    password = db.Column(db.Text)
    score = db.Column(db.Integer , nullable = False , default = 0)
    public_chats = db.relationship("PublicChat" , backref =  "user")
    player1s = db.relationship("Room" , backref = "player1" , foreign_keys = [Room.player1_id])
    player2s = db.relationship("Room" , backref = "player2" , foreign_keys = [Room.player2_id])

    def __init__(self , username , password ):
        self.username = username
        self.password = self.hash_password(password)

    
    def hash_password(self , password):
        return bcrypt.encrypt(password)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

    def __repr__(self):
        return self.username
