from flask import request, redirect, render_template, session, flash
from app import app, db
from models import Blog, User


@app.route('/')
def index():
    return redirect('/blog')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        username_error = ""
        password_error = ""

        if user and user.password == password:
            session['username'] = username
            flash('Logged in')
            return redirect('/newpost')
        elif not user:
            username_error = "incorrect username"
            return render_template("login.html", username=username,
            username_error=username_error, password_error=password_error)
        elif user and user.password != password:
            password_error = "incorrect password"
            return render_template("login.html", username=username,
            username_error=username_error, password_error=password_error)
    return render_template("login.html")
            

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blogs = Blog.query.all()
    if request.args.get('id'):
        id = request.args.get('id')
        title = Blog.query.filter_by(id=id).first().title
        body = Blog.query.filter_by(id=id).first().body
        return render_template("post.html", title=title, body=body)
    else:
        return render_template("blog.html", blogs=blogs)

@app.route('/newpost')
def newpost_entry():
    return render_template("newpost.html")

@app.route('/newpost', methods=['POST'])
def newpost():
    title = request.form['title']
    body = request.form['body']
    title_error = ""
    body_error = ""

    owner = User.query.filter_by(username=session['username']).first()

    if title == "":
        title_error = "Please fill in the title"
    if body == "":
        body_error = "Please fill in the body"

    if title_error or body_error:
        return render_template("newpost.html", title=title, title_error=title_error,
        body=body, body_error=body_error)

    else:
        new_post = Blog(title, body, owner)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/blog?id=" + str(new_post.id))

if __name__ == "__main__":
    app.run()