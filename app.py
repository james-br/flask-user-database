"""Blogly application."""
from flask import Flask, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    """Show home page"""
    return redirect("/users")

@app.route("/users")
def user_list():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html', users=users)

@app.route("/user/new", methods=["GET"])
def user_new_form():
    return render_template('add.html')

@app.route("/user/new", methods=["POST"])
def sub_new_user():

    new_user = User(first_name=request.form['first_name'], 
                    last_name=request.form['last_name'], 
                    image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show a page with info on a specific user"""

    user = user.query.get_or_404(user_id)
    return render_template('profile.html', user=user)