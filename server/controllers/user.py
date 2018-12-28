import datetime
from os import path
from sqlalchemy import func
from flask import render_template, Blueprint,redirect, url_for

from server.models import db,Log,User
from server.forms import LogForm

user_blueprint = Blueprint(
    'user',
    __name__,
    template_folder='../templates/user',
    url_prefix='/user'
)


@user_blueprint.route('/<string:username>')
def user(username):
    user = User.query.filter_by(username = username).first_or_404()

    return render_template(
            'user.html',
            user = user
    )

@user_blueprint.route('/feedback')
def feedback():
    form = LogForm()
    return render_template(
            'feedback.html',
            form=form
            )
