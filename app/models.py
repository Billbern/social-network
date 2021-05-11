from datetime import datetime
from app import db


class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=False, unique=True, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime)
    # followers = db.relationship('Follower', backref='follow', lazy='dynamic')
    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f"<User {self.username}>"


class Post(db.Model):
    
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    # userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, index=False, unique=False, nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime)

    def __repr__(self):
        return f'Post({self.content}, {self.createdAt})'


class Follower(db.Model):

    __tablename__ = 'follower'
    id = db.Column(db.Integer, primary_key=True)
    # sourceId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # targetId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime)


try:
    db.create_all()
except Exception as e:
    print(f'\n\n Error {e} \n\n')