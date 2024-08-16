# from functools import wraps
# from flask import Flask, abort, jsonify, request, session
# from flask_bcrypt import Bcrypt
# from flask_session import Session
# from flask_cors import CORS, cross_origin
# from models import db, User
# from config import ApplicationConfig
# from services.userService import CreateUser, GetUserById, GetUserByUsername

# app = Flask(__name__)
# app.config.from_object(ApplicationConfig)

# bcrypt = Bcrypt(app)
# serverSession = Session(app)
# CORS(app, supports_credentials=True)
# db.init_app(app)

# with app.app_context():
#     db.create_all()

# @app.route("/@me")
# def GetCurrentUser():
#     userId = session.get("user_id")
    
#     if not userId:
#         return jsonify({"error": "Unauthorized"}), 401
    
#     currentUser = GetUserById(userId)
    
#     return jsonify({
#         "id": currentUser.id,
#         "email": currentUser.email,
#         "username": currentUser.username,
#         "subscription": currentUser.subscription      
#     })
    

# @app.route("/registration", methods=["POST"])
# def registration():
#     newUser = CreateUser(bcrypt, request)
#     session["user_id"] = newUser.id
#     return jsonify({
#         "id": newUser.id,
#         "email": newUser.email,
#         "username": newUser.username,
#         "text3dCreditEqual" : newUser.text3dCreditEqual,
#         "image3dCreditEqual": newUser.image3dCreditEqual      
#     })


# @app.route("/login", methods=["POST"])
# def login_user():
#     username = request.json["username"]
#     password = request.json["password"]
    
#     user = GetUserByUsername(username)
    
#     if user is None:
#         return jsonify({"error": "Unauthorized"}), 401
    
#     if not bcrypt.check_password_hash(user.password, password):
#         return jsonify({"error": "Invalid credentials"}), 401

#     session["user_id"] = user.id
    
#     return jsonify({
#         "id": user.id,
#         "email": user.email,
#         "username": user.username,
#         "text3dCreditEqual" : user.text3dCreditEqual,
#         "image3dCreditEqual": user.image3dCreditEqual      
#     })
    
# @app.route("/logout", methods=["POST"])
# def LogOutUser():
#     session.pop("user_id", None)
#     return "200"

# def LoginRequired(f):
#     @wraps(f)
#     def DecoratedFunction(*args, **kwargs):
#         # Получаем session_id из куки
#         session_id_from_cookie = request.cookies.get('session_id')
#         # Проверяем, есть ли session_id в сессии и совпадает ли оно с тем, что в куке
#         if 'session_id' not in session or session['session_id'] != session_id_from_cookie:
#             return jsonify({'message': 'Unauthorized'}), 401
        
#         return f(*args, **kwargs)
    
#     return DecoratedFunction

# @app.route('/protected')
# @LoginRequired
# def protected():
#     return jsonify({'message': 'This is protected data'})

# if __name__ == "__main__":
#     app.run(debug=True)
from functools import wraps
from flask import Flask, jsonify, request, session, make_response
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS
from models import db, User
from config import ApplicationConfig
from services.userService import CreateUser, GetUserById, GetUserByUsername

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
serverSession = Session(app)
CORS(app, supports_credentials=True)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/@me")
def GetCurrentUser():
    userId = session.get("user_id")
    
    if not userId:
        return jsonify({"error": "Unauthorized"}), 401
    
    currentUser = GetUserById(userId)
    
    return jsonify({
        "id": currentUser.id,
        "email": currentUser.email,
        "username": currentUser.username,
        "subscription": currentUser.subscription      
    })
    

@app.route("/registration", methods=["POST"])
def registration():
    newUser = CreateUser(bcrypt, request)
    session["user_id"] = newUser.id
    return jsonify({
        "id": newUser.id,
        "email": newUser.email,
        "username": newUser.username,
        "text3dCreditEqual": newUser.text3dCreditEqual,
        "image3dCreditEqual": newUser.image3dCreditEqual      
    })


@app.route("/login", methods=["POST"])
def login_user():
    username = request.json.get("username")
    password = request.json.get("password")
    
    user = GetUserByUsername(username)
    
    if user is None:
        return jsonify({"error": "Unauthorized"}), 401
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    session["user_id"] = user.id
    
    # Устанавливаем флаг для отслеживания завершения логина
    response = make_response(jsonify({
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "text3dCreditEqual": user.text3dCreditEqual,
        "image3dCreditEqual": user.image3dCreditEqual      
    }))
    
    response.set_cookie('session_id', str(user.id), httponly=True)  # Устанавливаем куку сессии

    return response

@app.route("/logout", methods=["POST"])
def LogOutUser():
    session.pop("user_id", None)
    return "200"

def LoginRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id_from_cookie = request.cookies.get('session_id')
        user_id_from_session = session.get('user_id')
        
        if user_id_from_cookie is None or user_id_from_session is None or user_id_from_cookie != str(user_id_from_session):
            return jsonify({'message': 'Unauthorized'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

@app.route('/protected')
@LoginRequired
def protected():
    return jsonify({'message': 'This is protected data'})

if __name__ == "__main__":
    app.run(debug=True)
