# EStrade - Shipping Company Website
This repository contains the source code for a website for the shipping company EStrade. The website is built using Flask, a web framework for Python, and is designed to provide information about the company and its services.

## Features
* Displays information about the company and its services
* Contact form for users to send a message to the admin
* User's contact information is added to a database
* Admin page displays all user's contact information
* User receives an email with a predefined message after filling in the contact form
* Admin access to the website is restricted and requires a login

## Getting Started
To get started with this repository, you will need to have the following software installed:

* Python
* Flask

Once you have these installed, you can clone the repository to your local machine and run the following commands to set up the virtual environment:

pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

After setting up the virtual environment, you can run the following command to start the development server:

export FLASK_APP=app.py
flask run

You can access the website at `www.website.com`.

## Note
Please ensure that you have configured the email settings in the `config.py` file before running the website.

If you have any questions or issues with this repository, please open an issue on the GitHub page.
