import json as jsn
from app.models import *
from flask import render_template, jsonify
from app import app, socketio, emit, db, cross_origin


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def user_posts():
    return render_template('index.html', title="testing something")

@socketio.on('connect')
def connection():
    emit('display_posts', [{'id': item.id, 'content': item.content, 'createdAt': item.createdAt.isoformat(), 'updatedAt': item.updatedAt} for item in Post.query.all()])

@socketio.on('store_posts')
def store_post(post_data):
    new_post = Post(content=post_data)
    db.session.add(new_post)
    db.session.commit()
    emit('display_posts', [{'id': item.id, 'content': item.content, 'createdAt': item.createdAt.isoformat(), 'updatedAt': item.updatedAt} for item in Post.query.all()])
    
@socketio.on('display_posts')
def display_posts(data):
    emit('posts', data)
