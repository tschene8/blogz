from flask import Flask, request, redirect, render_template
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

@app.route('/blog', methods=['GET'])
def blog():
    id = request.args.get('id')
    if not id:
        blog = Blog.query.all()
        return render_template('blog.html', title="Build a Blog", blog=blog)
    else:
        post = Blog.query.get(id)
        return render_template('post.html', title=post.title, post=post)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_post = Blog(title, body)
        db.session.add(new_post)
        db.session.commit()
        return render_template('/blog?id=' + str(new_post))
    else:
        return render_template('newpost.html', title="Add Blog Entry")

if __name__ == '__main__':
    app.run()