from os import path
import bcrypt
from werkzeug.utils import secure_filename
from app.models import *
from flask import render_template, request, redirect, flash, url_for
from app import app, socketio, emit, db, session


@app.route('/', methods=['GET', 'POST'])
def user_posts():
    if 'user_id' in session:
        data = []
        if request.method == 'POST':
            if session['profile_id']:
                
                new_post = Post(author=session['profile_id'], content=request.form.get('formContent'))
                db.session.add(new_post)
                db.session.commit()

                upload_file = request.files.get('postimage')
                filename = secure_filename(upload_file.filename)
            
                if upload_file:
                    if filename == '' and f'.{filename.split(".")[1]}' not in app.config["UPLOAD_EXTENSIONS"]:
                        flash('select an image file', 'error')
                        return redirect('/')
                    upload_file.save(path.join(app.config['UPLOAD_PATH'], filename))
                    
                    new_img = Image(url=f'img/uploads/{filename}', description="nice post", owner=session["profile_id"], post=new_post.id)
                    db.session.add(new_img)
                    db.session.commit()

                flash('new post added successfully', 'info')
                return redirect('/')
            else:
                flash('you have to create a profile before you can post', 'error')
                return redirect('/')

        if session['profile_id']:
            for item in Post.query.filter(Post.author==session['profile_id']):
                if item.image:
                    data.append({'id': item.id, 'content': item.content, "image": [x.url for x in item.image], 'createdAt': item.createdAt.isoformat(), 'updatedAt': item.updatedAt})
                else:
                    data.append({'id': item.id, 'content': item.content, 'createdAt': item.createdAt.isoformat(), 'updatedAt': item.updatedAt})

        return render_template('index.html', title="testing something", data=data[::-1], user=session['user_name'])
    else:
        flash('you have to login first', 'error')
        return redirect('/auth/login')

@app.route('/profile/<username>', methods=['GET', 'POST'])
def handle_profile(username):
    if 'user_id' in session:
        if session['profile_id']:
            profile_data =  [{'firstname': data.firstname, 'lastname': data.lastname, 'email': data.email, 'image': data.image[0].url} for data in Profile.query.filter().join(Profile.image)]
            data = [{'id': item.id, 'content': item.content, 'createdAt': item.createdAt.isoformat(), 'updatedAt': item.updatedAt} for item in Post.query.filter(Post.author==session['profile_id'])]
        else:
            profile_data = ''
            data = []
        return render_template('profile.html', title=f"{username}'s Profile", data=data, profile=profile_data, user=session["user_name"])
    else:
        flash('you have to login first', 'error')
        return redirect('/auth/login')

@app.route('/profile/setting', methods=['GET', 'POST'])
def settings():
    if "user_id" in session:
        username = session["user_name"]
        
        if request.method == 'POST':
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            email = request.form.get('profile_email')
            
            new_profile = Profile(firstname=firstname, lastname=lastname, email=email, user=session['user_id'])
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

                session['profile_id'] = new_profile.id

                flash('profile has been updated', 'info')
                return redirect(f'/profile/{username}')
            

            session['profile_id'] = new_profile.id
            
            flash('profile has been updated', 'info')
            return redirect(f'/profile/{username}')

        return render_template('profileupdate.html', title="setting", user=session['user_name'])
    
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
            password = u"%s"%(request.form.get('userpass'))
            prospectiveuser = User.query.filter(User.username == username).first()
            if prospectiveuser:
                if bcrypt.checkpw(password.encode('utf-8'), prospectiveuser.password):
                    session['user_id'] = prospectiveuser.id
                    session['user_name'] = prospectiveuser.username
                    session['profile_id'] = ""
                    user_profile = [{'item': item.id} for item in Profile.query.filter(Profile.user == prospectiveuser.id)]
                    if len(user_profile) != 0:
                        session['profile_id'] = user_profile[0]['item']
                    flash('You have successfully logged in', 'info')
                    return redirect('/')
                else:
                    flash("username or password incorrect", "error")
                    return redirect('/auth/login')
            else:
                flash("username or password incorrect", "error")
                return redirect('/auth/login')

        return render_template('login.html', title="login Something")

@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        flash('you have already logged in', 'error')
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.form.get('username')
            password = u"%s"%(request.form.get('userpass'))
            confirmpass = u"%s"%(request.form.get('confirmpass'))
            if password == confirmpass:
                passhash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))
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
    
