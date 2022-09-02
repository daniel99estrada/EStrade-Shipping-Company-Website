from flask import Flask, render_template, request, redirect, url_for
from main import db, User, Message
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
        return "Name: {} {}, Email: {}".format(self.first_name, self.last_name, self.email)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), index=True)
    user_email = db.Column(db.Integer, db.ForeignKey('user.email'))

    def __repr__(self):
        return "{} - {}".format(self.message, self.user_email)


@app.route("/")
def homepage():
    return render_template('homepage.html')


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":

        # get data from html form.
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        gender = request.form.get('gender')
        message = request.form.get('message')
        
        new_user = User(first_name=first_name, last_name=last_name, email=email, gender=gender)
        message = Message(user_email=email, message=message)
        print("new user added")

        # Add user to database
        db.session.add(new_user)
        db.session.add(message)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

            # redirect to homepage
            return redirect(url_for('homepage'))

    return render_template('contact.html')


@app.route("/admin")
def admin():
    users = User.query.all()
    messages = Message.query.all()
    return render_template('admin.html', users=users, messages=messages)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host="0.0.0.0", port=100)