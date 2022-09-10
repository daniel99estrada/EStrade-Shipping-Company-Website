from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import os.path

app = Flask(__name__)

DB_NAME = "database"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), index=True)
    last_name = db.Column(db.String(80), index=True)
    email = db.Column(db.String(80), index=True, unique=True)
    phone_number = db.Column(db.String(80), index=True)
    message = db.relationship('Message', backref='User')

    def __repr__(self):
        return "Name: {} {}, Email: {}".format(self.first_name, self.last_name, self.email)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), index=True)
    date = db.Column(db.String(500), index=True)
    user_email = db.Column(db.Integer, db.ForeignKey('user.email'))

    def __repr__(self):
        return "{} - {} - {}".format(self.message, self.user_email, self.date)

class Admins(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), index=True)
    

from routes import *

if __name__ == '__main__':
    if not os.path.exists('database.db'):
        db.create_all()
    
    app.run(debug=True, host="0.0.0.0", port=100)