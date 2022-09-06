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


@app.route("/")
def homepage():
    return render_template('homepage.html')


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":

        # Check if email is already in the database
        user_exists = False
        email = request.form.get('email')

        inspector = inspect(db.engine)
        if (inspector.has_table("user")):
            user_exists = User.query.filter_by(email=email).first()

        if not user_exists:
            # Add user to database
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            gender = request.form.get('gender')
            
            new_user = User(first_name=first_name, last_name=last_name, email=email, gender=gender)
            db.session.add(new_user)
        
        # Add message to database
        date_obj = date.today()
        date_str = date_obj.strftime("%d/%m/%Y")
        message = request.form.get('message')

        message = Message(message=message, date=date_str, user_email=email)
        db.session.add(message)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

        send_email(email)

        return redirect(url_for('homepage'))

    return render_template('contact.html')


@app.route("/admin")
def admin():
    users = User.query.all()
    messages = Message.query.all()
    return render_template('admin.html', users=users, messages=messages, Message=Message)


if __name__ == '__main__':
    if not os.path.exists('database.db'):
        db.create_all()

    app.run(debug=True, host="0.0.0.0", port=100)