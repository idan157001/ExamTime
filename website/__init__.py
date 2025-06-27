from flask import Flask
from flask_cors import CORS
from flask import Blueprint
import secrets
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
GIMINI_API_KEY = os.environ.get('GIMINI_API_KEY')  # Set your API key for Gemini
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')  # Set your secret key for session management
if not APP_SECRET_KEY or not GIMINI_API_KEY:
    raise ValueError("Environment variables APP_SECRET_KEY and GIMINI_API_KEY must be set.")

main = Blueprint('main', __name__)

from . import routes

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY  # Set your secret key for session management

CORS(app)
app.register_blueprint(main)