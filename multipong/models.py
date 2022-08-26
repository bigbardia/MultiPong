from multipong.ext import db
from passlib.hash import bcrypt
from time import time

def gen_timestamp():
    return int(time())


class User(db.Model):

    _id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(20) , unique = True)
    password = db.Column(db.Text)
    score = db.Column(db.Integer , nullable = False , default = 0)
    public_chats = db.relationship("PublicChat" , backref =  "user")

    def __init__(self , username , password ):
        self.username = username
        self.password = self.hash_password(password)

    
    def hash_password(self , password):
        return bcrypt.encrypt(password)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

    def __repr__(self):
        return self.username

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
