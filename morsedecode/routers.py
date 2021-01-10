from flask import request, jsonify, session
from flask_login import login_user, logout_user, current_user

from . import app
from .models import *
from .morse_dictionary import from_morse

user_schema = UserSchema()
message_schema = MessageSchema()


@app.route('/register', methods=['POST'])
def register():
    errors = user_schema.validate(request.json)
    if errors:
        return jsonify(error="Mandatory Parameters not received"), 400
    
    user = User(username=request.json.get("username"), pswd=request.json.get("password"))
    if user.add():
        return jsonify(Message="Registration successful"), 201
    
    return jsonify(Message="User with same id already exists"), 400


@app.route('/decrypt', methods=['POST'])
def decrypt():
    if current_user.is_authenticated or session['logged_in']:
        encoded_message = request.json.get('message')
        if not encoded_message:
            return jsonify(Error="Message not received"), 400
        
        message = Message(message=from_morse(encoded_message), 
                          encoded_message=encoded_message, 
                          user_id=current_user.id)
        message.add()
        return jsonify(Message="Tranaslation saved"), 200
    return jsonify(Message="Not logged in!"), 400



@app.route('/login', methods=['POST'])
def login():
    errors = user_schema.validate(request.json)
    if errors:
        return jsonify(error="Mandatory Parameters not received"), 400
    
    user = User(username=request.json.get("username"), pswd=request.json.get("password"))
    if not user.verify_password(request.json.get("password")):
        return jsonify(Message="Credentials not verified"), 400
    
    login_user(user)
    session['logged_in'] = True
    return jsonify(Message="Logged in successfully"), 200


@app.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated or session['logged_in']:
        logout_user()
        session['logged_in'] = False
        return jsonify(Message="Logged out successfully"), 200
    return jsonify(Message="Not logged in!"), 400


@app.route('/mytranslations', methods=['GET'])
def translations():
    if current_user.is_authenticated or session['logged_in']:
        messages = Message.query.all()
        return jsonify(message_schema.dump(messages, many=True)), 200
    return jsonify(Message="Not logged in!"), 400
