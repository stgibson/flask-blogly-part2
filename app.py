"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "kubrick"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

@app.route("/")
def go_to_users_page():
    """
        Redirects user to the users page
        rtype: str
    """
    return redirect("/users")

@app.route("/users")
def show_user_list():
    """
        Shows a list of all users, along with an option to add a new user. Each
        user's name is linked to the user's profile.
        rtype: str
    """
    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template("users.html", users=users)

@app.route("/users/new")
def show_add_user_form():
    """
        Shows a form the user can fill out and submit to add a new user
        rtype: str
    """
    return render_template("add-user.html")

@app.route("/users/new", methods=["POST"])
def add_new_user():
    """
        Adds a new user using the info submitted from the form by the user, and
        then redirects back to the users page
        rtype: str
    """
    # first get info from form
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]

    # add new user to db
    new_user = None
    if image_url:
        new_user = User(first_name=first_name, last_name=last_name, \
            image_url=image_url)
    else:
        new_user = User(first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    """
        Goes to a page that gives detail about the user with id user_id
        type user_id: int
        rtype: str
    """
    user = User.query.get_or_404(user_id)
    
    return render_template("user-details.html", user=user)

@app.route("/users/<int:user_id>/edit")
def show_user_edit_form(user_id):
    """
        Goes to the edit user page for the user with id user_id
        type user_id: int
        rtype: str
    """
    user = User.query.get_or_404(user_id)

    return render_template("edit-user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """
        Edits details for the user with id user_id using info submitted from
        the form by the user, then redirects back to the users page
        type user_id: int
        rtype: str
    """
    # first get info from form
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]

    # update the user in the db
    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """
        Deletes user with id user_id, then redirects back to the users page
        type user_id: int
        rtype: str
    """
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def show_add_post_form(user_id):
    """
        Shows a form the user can fill out and submit to create a new post
        type user_id: int
        rtype: str
    """
    user = User.query.get_or_404(user_id)

    return render_template("add-post.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """
        Adds a new post for user with id user_id based on the info the user
        submitted in the form
        type user_id: int
        rtype: str
    """
    user = User.query.get(user_id)

    # get post details from form
    title = request.form["title"]
    content = request.form["content"]

    # create post and add to db
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_post_details(post_id):
    """
        Shows the title and content of post with id post_id, along with credits
        to the user who created the post, and options to go back to the user's
        page or to edit or delete the post
        type post_id: int
        rtype: str
    """
    post = Post.query.get_or_404(post_id)

    return render_template("post-details.html", post=post)