# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 12:06:04 2023

@author: aryan
"""

# Python standard libraries
import json
import os
import sqlite3



# Third-party libraries
from flask import Flask, redirect, request, url_for,render_template
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
import requests

# Internal imports
from db import init_db_command
from user import User

# Configuration
GOOGLE_CLIENT_ID = "332160652487-p0ddnke2i4sua458aouknm40h5o1h85d.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    if current_user.is_authenticated:
        
        """
        return (
            "<p>Hello, {}! You're logged in! </p>"
            "<p>Your Email: {}</p>"
            "<div><p>Your Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a> '.format(
                current_user.name, current_user.email, current_user.profile_pic
            )   
        )
    """
        return render_template("diamond.html", 
                               name=current_user.name, 
                               email=current_user.email, 
                               profile_pic=current_user.profile_pic)
    else:
        return(
            '<a class="button" href="/login">Google Login</a>'
              )

    
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="http://127.0.0.1:5000/callback/google",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/callback/google")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
    token_endpoint,
    authorization_response=request.url,
    redirect_url=request.base_url,
    code=code
    )
    token_response = requests.post(
    token_url,
    headers=headers,
    data=body,
    auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
            return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided by Google
    user = User(
    id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/diamond", methods=["GET", "POST"])
def diamond():
    diamond_pattern = ""
    if request.method == "POST":
        try:
            input_len = int(request.form["input_len"])

            if 1 <= input_len <= 100:
                diamond_pattern = generate_diamond_pattern(input_len)
            else:
                diamond_pattern = "Please enter a valid number between 1 and 100."
        except ValueError:
            diamond_pattern = "Please enter a valid number between 1 and 100."

    # Get user information if authenticated
    user_info = {}
    if current_user.is_authenticated:
        user_info["name"] = current_user.name
        user_info["email"] = current_user.email
        user_info["profile_pic"] = current_user.profile_pic

    return render_template("diamond.html", diamond_pattern=diamond_pattern, **user_info)



# Function to generate the diamond pattern
def generate_diamond_pattern(input_len):
    input_word = "FORMULAQSOLUTIONS"

    if input_len % 2 == 0:
        input_len += 1

    pyramid_1 = [j for j in range(input_len, 0, -2)][::-1]
    #pyramid_2 = [j for j in range(input_len, 0, -2)]

    bridge_word = " "

    increment = 0
    j = pyramid_1[increment]
    diamond_pattern = ""  # Initialize the diamond pattern as an empty string

    def append_diamond_pattern(word, spaces):
        nonlocal diamond_pattern
        diamond_pattern += " " * spaces + word + "\n"

    for i in range(len(input_word)):
        loop_word = ""
        for k in range(i, i + j):
            try:
                loop_word = loop_word + input_word[k]
            except IndexError:
                index = (j + i - k)
                loop_word = loop_word + input_word[:index]
                break
        spaces = len(input_word) - len(loop_word) // 2
        append_diamond_pattern(loop_word, spaces)

        increment += 1
        if increment >= len(pyramid_1):
            bridge_word = loop_word
            break
        j = pyramid_1[increment]

    i = 0
    loop_word = bridge_word
    main_count = increment
    increment = 0

    for k in range(i + 1, input_len - main_count + 1):
        loop_word = bridge_word[k:len(bridge_word) - k]
        spaces = len(input_word) - len(loop_word) // 2
        append_diamond_pattern(loop_word, spaces)

    return diamond_pattern # Return the generated diamond pattern as a string

    

if __name__ == '__main__':
    app.run(debug=True)
    