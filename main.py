from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
    gender = db.Column(db.String(80), index=True)

    def __repr__(self):
        return "Name:{} {}, Email: {}".format(self.first_name, self.last_name, self.email)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), index=True)
    user_email = db.Column(db.Integer, db.ForeignKey('user.email'))

    def __repr__(self):
        return "{} - {}".format(self.message, self.email)

import routes
