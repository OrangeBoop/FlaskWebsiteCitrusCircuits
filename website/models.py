from . import db # importing from the current package
from flask_login import UserMixin
from sqlalchemy.sql import func
import ast
from datetime import datetime


class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id')) #class User

class User(db.Model, UserMixin): #User Model - capital U because of python standarts
    id = db.Column(db.Integer,primary_key=True) #Id column counted by int with Primary Key!
    email = db.Column(db.String(150),unique=True) #unique - allows/forbids (False/True) multiple instances with same info 
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')# a list of all the nodes that a user owns
    cartItems = db.Column(db.String(150), default="Empty")
    Country = db.Column(db.String(150),nullable=False)
    comments = db.relationship('Comment', backref='user', lazy=True)
    def getUserId(user):
        return user.id

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    amountPaid = db.Column(db.Integer, nullable=False)
    orderItems = db.Column(db.String, nullable=False)
    orderDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # New column for order date
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    isOnSale = db.Column(db.Boolean, nullable=False, default=False)
    priceModifier = db.Column(db.Float, nullable=False, default=1)

class CommentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), unique=True, nullable=False)
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_data = db.Column(db.Text, nullable=False)
    comment_type = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

def getPrice(component):
    return component.price




    
