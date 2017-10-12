
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, name, body):
        self.slug = name
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_slug = request.form['slug']
        blog_body = request.form['body']
        new_blog = Blog(blog_slug, blog_body)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.all()
    return render_template('blog.html',title="My Blog", 
        blogs = blogs)
#~
#~
#~@app.route('/delete-task', methods=['POST'])
#~def delete_task():
#~
    #~task_id = int(request.form['task-id'])
    #~task = Task.query.get(task_id)
    #~task.completed = True
    #~db.session.add(task)
    #~db.session.commit()
#~
    #~return redirect('/')
#~

if __name__ == '__main__':
    app.run()
