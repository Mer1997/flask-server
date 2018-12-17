import datetime
from os import path
from sqlalchemy import func
from flask import render_template, Blueprint,redirect, url_for, flash
from server.forms import LogForm
from server.models import db,Log,User
logs_blueprint = Blueprint(
    'logs',
    __name__,
    template_folder='../templates/log',
    url_prefix='/log'
    )

@logs_blueprint.route('/<string:username>')
def logs(username):
    user = User.query.filter_by(username = username).first_or_404()
    logs = user.logs.order_by(Log.created.desc()).all()

    return render_template(
        'logs.html',
        user=user,
        logs=logs
    )

@logs_blueprint.route('/<string:username>/<int:log_id>')
def log(username, log_id):
    user = User.query.filter_by(username=username).first_or_404()
    log = user.logs.filter_by(log_id=log_id).first_or_404()
    return render_template(
        'log.html',
        user=user,
        log=log
    )

@logs_blueprint.route('/<string:username>/add',methods=['POST','GET'])
def addLog(username):
    user = User.query.filter_by(username = username).first_or_404()
    
    form = LogForm()

    if form.validate_on_submit():
        flash("The log has been added successful.",category='success')
        new_log = Log(form.info.data)
        new_log.user = user
        new_log.stat = 'Wait Process'
        new_log.created = datetime.datetime.now()

        db.session.add(new_log)
        db.session.commit()
        return render_template('log.html',user=user,log = new_log)
    flash("Invalid Log Info",category='warning')
    return render_template(
        'add.html',
        user=user,
        form = form
    )
