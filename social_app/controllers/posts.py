from social_app import app
from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
from social_app.models.user import User
from social_app.models.post import Post
import urllib.request
import os
from werkzeug.utils import secure_filename
import uuid as uuid



UPLOAD_FOLDER = 'social_app/static/img/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS






@app.route('/addPhoto', methods = ['GET', 'POST'])
def makePosts():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user'],
        'caption': request.form['caption']
    }
    file = request.files['media']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        media = str(uuid.uuid1()) + "_" + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], media))
        data['media'] = media
    else:
        return redirect(request.referrer)

    Post.makeContent(data)
    return redirect('/dashboard')





@app.route('/likePost/<int:id>')
def likeSomePost(id):
    data = {
        'post_id': id,
        'user_id': session['user']
    }
    Post.addLike(data)
    return redirect(request.referrer)





@app.route('/unlikePost/<int:id>')
def unlikeSomePost(id):
    data = {
        'post_id': id,
        'user_id': session['user']
    }
    Post.removeLike(data)
    return redirect(request.referrer)



@app.route('/addPhotos')
def addPhotos():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    loggedUser = User.getUserByID(data)
    return render_template("addPhotos.html", loggedUser = loggedUser)


@app.route('/createComment/<int:id>', methods = ['POST'])
def addComment(id):
    data = {
        'user_id': session['user'],
        'post_id': id,
        'content': request.form['content']
    }
    Post.komento(data)
    return redirect(request.referrer)

@app.route('/delete-post/<int:id>')
def destroyPost(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'post_id': id
    }
    currentPost = Post.getPostById(data)
    if session['user'] != currentPost['user_id']:
        return redirect('/404')
    Post.deletePost(data)
    return redirect(request.referrer)
    

@app.route('/delete-comment/<int:id>')
def deleteComment(id):
    data = {
        'id': id,
        'user_id': session['user']
    }
    currentComment = Post.getCommentByID(data)
    if session['user'] != currentComment['user_id']:
        return redirect('/404')
    Post.removeComment(data)
    return redirect(request.referrer)