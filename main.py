
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


@app.route('/new_post', methods=['POST', 'GET'])
def new_post(): 
    return render_template('newpost.html', title="New Blog Post")
    
@app.route('/redirect', methods=['GET','POST'])
def new_post_redirect():
    if request.method == 'POST':
        blog_slug = request.form['slug']
        blog_body = request.form['body']
        if blog_slug == "":
            return render_template('newpost.html', title='New Blog Post', error1 = "Give your post a title!")
        if blog_body == "":
            return render_template('newpost.html', title='New Blog Post', error2 = "This isn't twitter, write something!")
        new_blog = Blog(blog_slug, blog_body)
        db.session.add(new_blog)
        db.session.commit()
    id = Blog.query.order_by(Blog.id.desc()).first().id
    
    return redirect("/blog?id="+str(id))
    

@app.route('/blog', methods = ['POST','GET'])
def index():
    if request.args.get('id') != None:
        id = request.args.get('id')
        entry = Blog.query.filter(Blog.id==id).one()
        return render_template('blog-post.html', entry = entry)
    else:
        blogs = Blog.query.all()
        return render_template('blog.html',title="My Blog", 
            blogs = blogs)
        
@app.route('/', methods=['GET'])
def get_start():
    return redirect('/blog')




if __name__ == '__main__':
    app.run()
