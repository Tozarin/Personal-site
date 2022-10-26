import sys

from flask import Flask, render_template, request, flash, url_for, redirect

from config import SQLITE_DATABASE_NAME
from model import db, db_init, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + SQLITE_DATABASE_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "anti-amogus"
db.app = app
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():

    ps = Post.query.order_by(Post.id.desc()).all()

    if request.method == 'POST':
        name = request.form.get('name', type=str, default='')
        text = request.form.get('text', type=str, default='')

        if not name:
            flash('Пожлуйста, укажите своё имя!')
            return render_template('index.html', posts=ps)

        if not text:
            flash('Отзыв не может быть пустым.')
            return render_template('index.html', posts=ps)

        try:
            post = Post(name=name, text=text)
            db.session.add(post)
            db.session.commit()
        except:
            print('Fatall error wile adding new post')

        ps = Post.query.order_by(Post.id.desc()).all()

        return render_template('index.html', posts=ps)

    return render_template('index.html', posts=ps)

@app.route('/guestbook')
def guest_book():

    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('guestbook.html', posts=posts)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == 'init':
            with app.app_context():
                db_init()
                sys.exit(0)

    app.run(port=5000, debug=True)