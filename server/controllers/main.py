import datetime
from os import path
from sqlalchemy import func
from flask import render_template, Blueprint,redirect, url_for, flash

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


@main_blueprint.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash("Your have been logged in.", category="success")
        user = User.query.filter_by(username=form.username.data).first()
        return render_template(
            'user.html',
            user=user
        )
    return render_template('login.html',form=form)
