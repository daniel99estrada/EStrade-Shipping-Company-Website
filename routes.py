from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy, inspect
import os.path
from datetime import date
from sendEmails import send_email
from main import db, User, Message, app
from __main__ import app


@app.route("/")
def homepage():
    return render_template('homepage.html')


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":

        # Check if email is already in the database
        email = request.form.get('email')
        user_exists = False
        
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

        #send_email(email)
        return redirect(url_for('homepage'))

    return render_template('contact.html')


@app.route("/admin")
def admin():
    users = User.query.all()
    messages = Message.query.all()
    return render_template('admin.html', users=users, messages=messages)