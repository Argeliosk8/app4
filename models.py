from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    joined_at = db.Column(db.DateTime(), index = True, default = datetime.utcnow)
    vehicles = db.relationship('Vehicle', backref = 'owner', lazy = 'dynamic', cascade = 'all, delete, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    brand = db.Column(db.String(150))
    model = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


db.create_all()




