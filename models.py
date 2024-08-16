from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from uuid import uuid4
db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class Subscription(db.Model):
    id = db.Column(db.String(64), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(16), unique=True)
    price = db.Column(db.Float, nullable=False)
    text3dCreditEqual = db.Column(db.Float)
    image3dCreditEqual = db.Column(db.Float)
    

    users = db.relationship("User", back_populates="subscription")

class User(db.Model):
    id = db.Column(db.String(64), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(32), unique=True)
    text3dCreditEqual = db.Column(db.Float)
    image3dCreditEqual = db.Column(db.Float)
    
    subscription_id = db.Column(db.String(64), db.ForeignKey('subscription.id'))
    

    subscription = db.relationship("Subscription", back_populates="users")
    
