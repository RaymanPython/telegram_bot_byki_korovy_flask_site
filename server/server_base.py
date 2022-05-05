from flask import Flask
from flask import request, abort, render_template, redirect
import json
import sqlite3
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
import datetime
from sqlalchemy import orm
from data.users import User
from data import db_session
from flask import json
from forms.user import RegisterForm




app = Flask(__name__)

NAME_FILE = 'main.db'




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/users_all')
def users_all():
    db_sess = db_session.create_session()
    users = []
    for user in db_sess.query(User).all():
        users.append(str(user))
    return render_template('all_users.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/index')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/users/', methods=['POST'])
def users():

    if request.method == 'POST':
        data = json.loads(request.data)
        print(data)
        username = data['username']
        realname = data['real_name']
        records = data['records']
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == username).first()
        print(user)
        if user == None:
            user = User()
            user.username = username
            db_sess.add(user)
        user.realname = realname
        user.records = str(records)
        user.created_date = datetime.datetime.now()
        db_sess.commit()
        return '5'
    else:
        abort(405)


@app.before_first_request
def startup():
    db_session.global_init("db/blogs.db")
    # user = User()
    # user.name = "Пользователь 1"
    # user.records = "Молодец"
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()




if __name__ == "__main__":
    app.run()