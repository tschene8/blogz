from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:1234@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect('/blog')

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
def display_entry_form():
    return render_template("newpost.html")

@app.route('/newpost', methods=['POST'])
def newpost():
    title = request.form['title']
    body = request.form['body']
    title_error = ""
    body_error = ""

    if title == "":
        title_error = "Please fill in the title"
    if body == "":
        body_error = "Please fill in the body"

    if title_error or body_error:
        return render_template("newpost.html", title=title, title_error=title_error,
        body=body, body_error=body_error)

    else:
        new_post = Blog(title, body)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/blog?id=" + str(new_post.id))

if __name__ == "__main__":
    app.run()