from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy, inspect
import os.path
from datetime import date
from sendEmails import send_email

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

from routes import *

if __name__ == '__main__':
    if not os.path.exists('database.db'):
        db.create_all()
    
    app.run(debug=True, host="0.0.0.0", port=100)