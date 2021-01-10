from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import fields, Schema
from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password = db.Column(db.String)
    messages = db.relationship('Message', backref='users', lazy='dynamic')

    def __init__(self, username, pswd):
        self.username = username
        self.password = pswd
    
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, plaintext):
        self._password = generate_password_hash(plaintext, "sha256")

    def verify_password(self, plaintext):
        user = self.check()
        if user:
            return check_password_hash(user.password, plaintext)
        return False

    def check(self):
        return db.session.query(User).filter_by(username=self.username).first()
    
    def add(self):
        if not self.check():
            db.session.add(self)
            db.session.commit()
            return True
        return False

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    encoded_message = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, message, encoded_message, user_id):
        self.message = message
        self.encoded_message = encoded_message
        self.user_id = user_id

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class MessageSchema(Schema):
    user_id = fields.Int(required=True)
    message = fields.Str(required=True)
    encoded_message = fields.Str(required=True)
