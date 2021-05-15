from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit, send
from app.config import Config

app = Flask(__name__, static_url_path="", static_folder="public")

app.config.from_object(Config)

Session(app)
cors = CORS(app)
db = SQLAlchemy(app)

socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)

from app import views

try:
    db.create_all()
except Exception as e:
    print(f'\n\n Error {e} \n\n')