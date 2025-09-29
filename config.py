import os

# Define the base directory of the application
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Base configuration class. Contains settings common to all environments.
    """
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-hard-to-guess-string'

    # --- UPDATED DATABASE CONFIGURATION ---
    # This logic now prioritizes a production DATABASE_URL (from AWS RDS).
    # If it doesn't exist, it falls back to the local SQLite database for development.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # Disable a feature that signals the application on every database change
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Folder for uploaded post images
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/post_images')

    # --- MAIL SERVER SETTINGS ---
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['getintouch.spiconsulting@gmail.com'] # The email that will receive messages

