from os import path
import bcrypt
from werkzeug.utils import secure_filename
from app.models import *
from flask import render_template, request, redirect, flash, url_for
from app import app, socketio, emit, db, session


@app.route('/', methods=['GET', 'POST'])
def user_posts():
    if 'user_id' in session:
        if request.method == 'POST':
            if 'profile_id' in session:
                new_post = Post(author=session['profile_id'], content=request.form.get('formContent'))
                db.session.add(new_post)
                db.session.commit()
                flash('new post added successfully', 'info')
                return redirect('/')
            else:
                flash('you have to create a profile before you can post', 'error')
                return redirect('/')

        if 'profile_id' in session:
            data = [{'id': item.id, 'content': item.content, 'createdAt': item.createdAt.isoformat(), 'updatedAt': item.updatedAt} for item in Post.query.filter(Post.author==session['profile_id'])]
        else:
            data = []

        return render_template('index.html', title="testing something", data=data, user=session['user']['user_name'])
    else:
        flash('you have to login first', 'error')
        return redirect('/auth/login')

@app.route('/profile/<username>', methods=['GET', 'POST'])
def handle_profile(username):
    if 'user' in session:
        if request.method == 'POST':
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            email = request.form.get('profile_email')

            new_profile = Profile(firstname=firstname, lastname=lastname, email=email, user=session['user']['id'])
            db.session.add(new_profile)
            db.session.commit()

            upload_file = request.files.get('imageupload')
            filename = secure_filename(upload_file.filename)

            if upload_file:
                if filename == '' and f'.{filename.split(".")[1]}' not in app.config["UPLOAD_EXTENSIONS"]:
                    flash('select an image file', 'error')
                    return redirect(f'/profile/{username}')
                upload_file.save(path.join(app.config['UPLOAD_PATH'], filename))
                
                new_img = Image(url=f'img/uploads/{filename}', description="profile picture", owner=new_profile.id)
                db.session.add(new_img)
                db.session.commit()
                flash('profile has been updated', 'info')
                return redirect(f'/profile/{username}')
            
            flash('profile has been updated', 'info')
            return redirect('/')
        else:
            return render_template('profile.html', title=f"{username}'s Profile")
    else:
        flash('you have to login first', 'error')
        return redirect('/auth/login')

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        flash('you have already logged in', 'error')
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.form.get('username')
            password = bytes(request.form.get('userpass'), 'utf-8')
            prospectiveuser = User.query.filter(User.username == username).first()
            if prospectiveuser:
                if bcrypt.checkpw(password, prospectiveuser.password):
                    session['user_id'] = prospectiveuser.id
                    session['user_name'] = prospectiveuser.username
                    try:
                        user_profile = Profile.query.filter(Profile.user == prospectiveuser.id)
                        session['user'] = {'id': prospectiveuser.id, 'user_name': prospectiveuser.username, 'profile_id': user_profile.id}
                    except:
                        session['user'] = {'id': prospectiveuser.id, 'user_name': prospectiveuser.username, 'profile_id': 0}
                    flash('You have successfully logged in', 'info')
                    return redirect('/')
                else:
                    flash("username or password incorrect", "error")
                    return redirect('/auth/login')
            else:
                flash("username or password incorrect", "error")
                return redirect('/auth/login')

        return render_template('login.html', title="Login Something")

@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        flash('you have already logged in', 'error')
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.form.get('username')
            password = bytes(request.form.get('userpass'), 'utf-8')
            confirmpass = bytes(request.form.get('confirmpass'), 'utf-8')
            if password == confirmpass:
                passhash = bcrypt.hashpw(password, bcrypt.gensalt(10))
                new_user = User(username=username, password=passhash)
                db.session.add(new_user)
                db.session.commit()
                flash('Account successfully created log in to proceed', 'info')
                return redirect('/auth/login')
            else:
                flash('passwords do not match', 'error')
                return redirect('/auth/register')
                
        return render_template('register.html', title="Register Something")

@app.route('/auth/logout', methods=['Get'])
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('profile_id', None)
    return redirect('/auth/login')

@app.route('/edit/<id>', methods=['PUT'])
def edit_post(id):
    pass

@app.route('/delete/<id>', methods=["DELETE"])
def delete_post(id):
    pass

@socketio.on('handleChange')
def handleChange(data):
    if(data['method'] == 'edit'):
        print('editing...')
    else:
        Post.query.filter_by(id=data['item']).delete()
        db.session.commit()
    emit('display_posts', [{'id': item.id, 'content': item.content, 'createdAt': item.createdAt.isoformat(), 'updatedAt': item.updatedAt} for item in Post.query.all()])
    
