"""Blogly application."""
from flask import Flask, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post



app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def root():
    return redirect("/users")


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""
    return render_template('404.html'), 404

@app.route("/users")
def user_list():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html', users=users)

@app.route("/users/new", methods=["GET"])
def user_new_form():
    return render_template('add.html')

@app.route("/users/new", methods=["POST"])
def sub_new_user():

    new_user = User(first_name=request.form['first_name'], 
                    last_name=request.form['last_name'], 
                    image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>')
def users_show(user_id):
    
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.fullname} was deleted.")
    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def mew_post_form(user_id):
    """Creates a form for users to post comments"""
    user = User.query.get_or_404(user_id)
    return render_template('new.html', user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_post(user_id):
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)
    db.session.add(new_post)
    db.session.commit()
    flash(f"new post was created: {new_post.title}")
    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post has been edited: {post.title}")
    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post has been deteled:{post.title}")
    return redirect(f"/users/{post.user_id}")