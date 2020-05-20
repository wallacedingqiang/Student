from flask import Flask, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy  # pyhton3 必须用这种方式导入
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
import pymysql
from sqlalchemy import desc


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./atm_data.db'  # 相对路径
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# 定义ORM


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name
# 创建表格、插入数据


@app.before_first_request
def create_db():
    # Recreate database each time for demo
    db.drop_all()
    db.create_all()
    admin = User('admin', 'admin@example.com')
    db.session.add(admin)
    guestes = [User('guest1', 'guest1@example.com'),
               User('guest2', 'guest2@example.com'),
               User('guest3', 'guest3@example.com'),
               User('guest4', 'guest4@example.com')]
    db.session.add_all(guestes)
    db.session.commit()


# 查询
@app.route('/user')
def users():
    users = User.query.all()
    return "<br>".join(["{0}: {1}".format(user.name, user.email)
                        for user in users])


@app.route('/userlist',methods=['GET', 'POST'])
def userslist():
    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/')
@app.route('/index')
def index():
  user = {'nickname': 'Miguel'}  # fake user
  posts = [  # fake array of posts
    {
      'author': {'nickname': 'John'},
      'body': 'Beautiful day in Portland!'
    },
    {
      'author': {'nickname': 'Susan'},
      'body': 'The Avengers movie was so cool!'
    }
  ]
  return render_template("indexold.html",
                         title='Home',
                         user=user,
                         posts=posts)


# 查询
@app.route('/user/<int:id>')
def user(id):
    user = User.query.filter_by(id=id).one()
    return "{0}: {1}".format(user.name, user.email)


# 运行
if __name__ == '__main__':
    app.run('127.0.0.1', 5000)
