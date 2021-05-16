from datetime import datetime
from app import db


followers = db.Table('followers',
        db.Column('follower_id', db.Integer, db.ForeignKey('profile.id')), 
        db.Column('followed_id', db.Integer, db.ForeignKey('profile.id'))
)

likes = db.Table('likes', 
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')), 
                db.Column('user_id', db.Integer, db.ForeignKey('profile.id'))
)

class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=False, unique=True, nullable=False)
    password = db.Column(db.LargeBinary(), index=False, unique=True, nullable=False)
    profile = db.relationship('Profile', backref='metadata', uselist=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime)

    def __repr__(self):
        return f"<User {self.username}>"

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), index=True, unique=True, nullable=False)
    isOnline = db.Column(db.Boolean)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    image = db.relationship('Image', backref='picture')
    notification = db.relationship('Notification', backref='news')
    followed = db.relationship(
        'User', secondary=followers, 
        primaryjoin=(id == followers.c.follower_id),  
        secondaryjoin=(id == followers.c.followed_id), 
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )
    message_sent = db.relationship('Message', foreign_keys='Message.sender', backref="sent", lazy='dynamic')
    message_received = db.relationship('Message', foreign_keys='Message.recipient', backref="received", lazy='dynamic')
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime)

class Post(db.Model):
    
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    content = db.Column(db.Text, index=False, unique=False, nullable=True)
    image = db.relationship('Image', backref='media')
    likes = db.relationship('Profile', secondary=likes, backref=db.backref('likes', lazy='dynamic'))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime)

    def __repr__(self):
        return f'Post({self.content}, {self.createdAt})'

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('profile.id'))
    post = db.Column(db.Integer, db.ForeignKey('post.id'))


class Message(db.Model):

    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    sender = db.Column(db.Integer, db.ForeignKey('profile.id'))
    recipient = db.Column(db.Integer, db.ForeignKey('profile.id'))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime)


class Notification(db.Model):

    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    seen = db.Column(db.Boolean, default=False)
    content = db.Column(db.Text, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('profile.id'))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)


class Sessions(db.Model):

    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True)
    data = db.Column(db.LargeBinary)
    expiry = db.Column(db.DateTime)
