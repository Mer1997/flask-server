import datetime
from os import path
from sqlalchemy import func
from flask import render_template, Blueprint,redirect, url_for

from server.models import db,Log,User
from server.forms import UsernameForm,PasswordForm

setting_blueprint = Blueprint(
    'setting',
    __name__,
    template_folder=path.join(path.pardir,'templates','setting'),
    url_prefix="/setting"
)

@setting_blueprint.route('/<string:username>/admin')
def admin(username):
    user = User.query.filter_by(username = username).first_or_404()

    return render_template(
        'admin.html',
        user = user
    )

@setting_blueprint.route('/<string:username>/change_password', methods=['GET','POST'])
def changePassword(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = PasswordForm()
    if form.validate_on_submit():
        if form.old_pwd.data == user.password and form.new_pwd.data == form.confirm_pwd.data:
            user.password = form.new_pwd.data
        return render_template(
            'user.html',
            user=user
        )
    return render_template(
            'cpwd.html',
            user=user,
            form=form
        )

@setting_blueprint.route('/<string:username>/change_username')
def changeUsername(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = UsernameForm()
    if form.validate_on_submit():
        is_existed = User.query.filter_by(username=form.new_name.data).first()
        if not is_existed:
            User.query.filter_by(username=username).first_or_404().update({
                    'username': form.new_name.data
                })
            db.session.commit()
        else:
            pass
        return render_template(
            'user.html',
            user=user
        )
    return render_template(
            'cuname.html',
            user=user,
            form=form
        )

