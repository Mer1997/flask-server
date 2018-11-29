import datetime
from os import path
from sqlalchemy import func
from flask import render_template, Blueprint,redirect, url_for

from server.models import db,Log,User

user_blueprint = Blueprint(
    'user',
    __name__,
    template_folder=path.join(path.pardir,'templates','user'),
    url_prefix='/user'
)


@user_blueprint.route('/<string:username>')
def user(username):
    user = User.query.filter_by(username = username).first_or_404()

    return render_template(
            'user.html',
            user = user
    )


