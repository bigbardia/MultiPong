from multipong.ext import db
from uuid import uuid4
from passlib.hash import bcrypt


class User(db.Model):

    _id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(20) , unique = True)
    password = db.Column(db.Text)
    score = db.Column(db.Integer , nullable = False , default = 0)
    # public_chats = db.relationship()

    def __init__(self , username , password ):
        self.username = username
        self.password = self.hash_password(password)

    
    def hash_password(self , password):
        return bcrypt.encrypt(password)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

    def __repr__(self):
        return self.username

# class PublicChat(db.Model):

#     _id = db.Column(db.Integer, primary_key = True)
#     text = db.Column(db.Text , nullable = False)
#     timestamp = db.Column(db.Integer, nullable= False , default = "")

#     def __init__(self ,text):
#         self.text = text