import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    CORS_HEADERS = os.environ.get('CORS_HEADERS')
    SESSION_TYPE = os.environ.get('SESSION_TYPE')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif', '.webm']
    MAX_CONTENT_LENGTH = 1024*1024
    UPLOAD_PATH = './app/public/img/uploads/'