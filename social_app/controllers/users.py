from social_app import app
from flask import render_template, request, redirect, session, flash, jsonify
from flask_bcrypt import Bcrypt

from social_app.models.user import User
from social_app.models.post import Post
import urllib.request
import os
from werkzeug.utils import secure_filename
import uuid as uuid
import json

bcrypt = Bcrypt(app)


UPLOAD_FOLDER = 'social_app/static/img/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def loginRegister():
    if 'user' in session:
        return redirect('/dashboard')
    return render_template("login.html")

@app.route('/register')
def registerPage():
    if 'user' in session:
        return redirect('/dashboard')
    return render_template("register.html")


@app.route('/addProfilePic', methods = ['GET','POST'])
def uploadPhoto():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    file = request.files['profile_pic']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        profile_pic = str(uuid.uuid1()) + "_" + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_pic))
        data['profile_pic'] = profile_pic
        print(data)
    else:
        flash("Allowed image types are .png, .jpg, .jpeg", 'allowedError')
        return redirect(request.referrer)

    User.updateUserPhoto(data)
    return redirect(request.referrer)


@app.route('/updateInfoAboutUser', methods = ['POST'])
def update():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user'],
        'username': request.form['username'],
        'about': request.form['about']
    }
    User.updateUserInfo(data)
    return redirect(request.referrer)





@app.route('/dashboard')
def smth():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    loggedUser = User.getUserByID(data)
    posts = Post.getPosts()
    likes = Post.likeUnlike(data)
    request = User.getAllRequestReceived(data)
    connect = User.getNumberOfConnections(data)
    return render_template("dashboard.html", loggedUser = loggedUser, posts = posts, likes = likes, request= request, connect =connect)

@app.route('/profileUser/<int:id>')
def otherUserProfile(id):
    data = {
        'user_id': id
    }
    data2 = {
        'user_id': session['user']
    }
    loggedUser = User.getUserByID(data2)
    otherUser = User.getUserByID(data)
    likes = Post.likeUnlike(data2)
    connect = User.getNumberOfConnections(data)
    posts = User.getUserPosts(data)
    friends = User.getAllFriends(data)
    print(otherUser)
    return render_template("othersProfile.html", otherUser = otherUser, likes = likes, connect = connect, posts = posts, friends = friends, loggedUser = loggedUser)


@app.route('/profile/<int:id>')
def profile(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    loggedUser = User.getUserByID(data)
    posts = User.getUserPosts(data)
    requestSentTo = User.getSentRequest(data)
    allUsersBesidesMe = User.getAllUsersToSendRequest(data)
    friends = User.getAllFriends(data)
    likes = Post.likeUnlike(data)
    connect = User.getNumberOfConnections(data)
    return render_template("profile.html", loggedUser = loggedUser, posts = posts, users = allUsersBesidesMe, requestsSend = requestSentTo, friends= friends, likes= likes ,connect = connect)

@app.route('/search', methods = ['POST'])
def searchForUser():
    data = {
        'username': request.form['username']
    }
    users = [c for c in User.searchUser(data) if str(data).lower() ] 
    return jsonify({'results': users})


@app.route('/deleteRequest/<int:id>')
def deleteRequest(id):
    data = {
        'loggedUser_id': session['user'],
        'receiver_id': id,
    }
    User.deleteRequest(data)
    return redirect(request.referrer)


@app.route('/addFriend/<int:id>')
def makeFriend(id):
    data = {
        'loggedUser_id': session['user'],
        'receiver_id': id,
        'status' : 0
    }
    User.makeFriendRequest(data)
    return redirect(request.referrer)



@app.route('/acceptFriendship/<int:id>')
def acceptFriendship(id):
    data = {
        'loggedUser_id': session['user'],
        'friend_id': id,
    }
    User.approveRequest(data)
    return redirect(request.referrer)


@app.route('/rejectFriendship/<int:id>')
def rejectFriendship(id):
    data = {
        'loggedUser_id': id,
        'receiver_id':  session['user'],
    }
    User.rejectRequest(data)
    return redirect(request.referrer)


@app.route('/createUser', methods=['POST'])
def createAccount():
    if 'user' in session:
        return redirect(request.referrer)
    if not User.validateUser(request.form):
        flash("Something is wrong, check the errors", 'signUpError')
        return redirect(request.referrer)
    if User.getUserByEmail(request.form):
        flash("This email already exists, try another one", 'emailRegister')
        return redirect(request.referrer)
        
    data = {
        'username': request.form['username'],
        'email' : request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.addUser(data)
    flash("You can now login", 'signUpSuccess')
    return redirect(request.referrer)




@app.route('/logAcc', methods = ['POST'])
def loginUser():
    if 'user' in session:
        return redirect(request.referrer)
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }
    if not User.getUserByEmail(data):
        flash("This email doesn't exit, try again", 'emailLogin')
        return redirect(request.referrer)
    user = User.getUserByEmail(data)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Incorrect password", 'passwordLogin')
        return redirect(request.referrer)

    session['user'] = user['id']
    return redirect('/dashboard')

@app.route('/getEmails')
def getEmail():
    return jsonify(User.getUserByEmail(request.form))



@app.route('/404')
def error():
    return render_template("404.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

