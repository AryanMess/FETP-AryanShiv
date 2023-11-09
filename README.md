# FETP-AryanShiv
Creating a Flask Application containing Google's OAuth 2 Application for Login 

    
![Architecture](https://www.tutorialspoint.com/oauth2.0/images/OAuth_diagram.jpg)

Flask Web Application with Google OAuth 2.0 Authentication Documentation



Introduction

This documentation outlines the development of a web application using Flask, a Python web framework, and integrates Google OAuth 2.0 for user authentication. The application allows users to log in with their Google accounts, displays user information, and features a dynamic display of the current time.
Table of Contents

    Requirements
    Setup
    File Structure
    Functionality
        User Authentication
        Display User Information
        Dynamic Time Display

Requirements

    Python
    Flask
    Flask-Login
    OAuthlib
    Requests

Ensure that these dependencies are installed before running the application.
Setup

    Google API Credentials:
        Obtain Google API credentials by creating a project on the Google Cloud Console.
        Note the client ID and client secret.

    Environment Variables:
        Set the GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables in your system or within the application.

    Run the Application:
        Execute the app.py file to start the Flask development server.

File Structure

The application consists of the following key files and directories:

    app.py: Main application file containing Flask routes and configuration.
    templates: Directory containing HTML templates for rendering pages.

Functionality
User Authentication

    Users can log in using their Google accounts.
    The application utilizes Flask-Login for user session management.

Display User Information

    Upon successful login, users are presented with a personalized welcome message, their email, and Google profile picture.
    The user information is dynamically retrieved from the Google OAuth 2.0 provider.

Dynamic Time Display

    The web page displays the current time below the user's profile picture.
    JavaScript is used to update the time every second, providing a dynamic user experience.

This documentation now focuses on the key aspects of the Flask web application and removes references to specific modules.
