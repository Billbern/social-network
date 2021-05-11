import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_url_path="", static_folder="public")
cors = CORS(app)
app.config['CORS_HEADERS'] = os.environ.get('CORS_HEADERS')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

from app import views