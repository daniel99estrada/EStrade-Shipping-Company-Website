from main import app
from main import db, User, Message
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


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
        mesage = request.form.get('message')
        
        new_user = User(first_name=first_name, last_name=last_name, email=email, gender=gender)
        #message = Message(user_email=email, message=message)
        print("new user added")

        # Add user to database
        db.session.add(new_user)
        #db.session.add(message)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

            #redirect to homepage
            #return redirect(url_for('homepage'))

    return render_template('contact.html')


@app.route("/admin")
def admin():
    users = User.query.all()
    #messages = Message.query.all()
    return render_template('admin.html', users = users)



