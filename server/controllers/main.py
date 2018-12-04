import datetime,logging
from os import path
from sqlalchemy import func
from flask import render_template, Blueprint,redirect, url_for, flash
from flask_wtf import FlaskForm
from server.models import db,Log,User
from server.forms import LoginForm, RegisterForm

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates/main'
)

@main_blueprint.route('/')
def index():
    return render_template(
        'index.html'
    )

@main_blueprint.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash("Your have been logged in.", category="success")
        user = User.query.filter_by(username=form.username.data).first()
        logging.info('Login Successful')
        return render_template(
            'user.html',
            user=user
        )
    return render_template('login.html', form = form)


@main_blueprint.route('/logout',methods=['GET','POST'])
def logout():
    return render_template(
            'index.html',
    )

@main_blueprint.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.username.data)
        new_user.setPassword(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash("Your user has been created, please login.", category="success")
        return redirect(url_for('.login'))

    return render_template('register.html',form=form)


