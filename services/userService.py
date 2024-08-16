from flask import request, abort
from models import db, User

def CreateUser(bcrypt, request):
    email = request.json["email"]
    password = request.json["password"]
    username = request.json["username"]
        
    userExists = User.query.filter(User.email==email).first() is not None
    
    if userExists:
        abort(409)
        
    hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
    newUser = User(email=email,username=username, password=hashedPassword, text3dCreditEqual = 3, image3dCreditEqual = 3)
    db.session.add(newUser)
    db.session.commit()
    
    return newUser


def GetUserById(id):
    return User.query.filter(User.id==id).first()

def GetUserByUsername(username):
    return User.query.filter(User.username==username).first()