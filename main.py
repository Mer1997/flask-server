from flask import Flask, render_template
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text,unique = True)
    password = db.Column(db.Text, unique = True)
    logs = db.relationship(
        'Log',
        backref='user',
        lazy='dynamic'
    )

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class Log(db.Model):
    log_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime())
    info = db.Column(db.Text)
    stat = db.Column(db.Text)

    def __init__(self, info):
        self.info = info

    def __repr__(self):
        return "<Log '{}'>".format(self.info)


class PasswordForm(Form):
    old_pwd = StringField(
       'Old_pwd',
       validators=[DataRequired(),Length(min=6,max=16)]
    )
    new_pwd = StringField(
       'New_pwd',
       validators=[DataRequired(),Length(min=6,max=16)]
    )
    confirm_pwd = StringField(
       'Confirm_pwd',
       validators=[DataRequired(),Length(min=6,max=16)]
    )
    
class UsernameForm(Form):
    new_name = StringField(
       'New_name',
       validators=[DataRequired(),Length(min=4,max=16)]
    )


@app.route('/<string:username>')
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    
    return render_template(
            'user.html',
            user = user
    )

@app.route('/<string:username>/logs')
def logs(username):
    user = User.query.filter_by(username = username).first_or_404()
    logs = user.logs.order_by(Log.created.desc()).all()

    return render_template(
        'logs.html',
        user=user,
        logs=logs
    )

@app.route('/<string:username>/logs/<int:log_id>')
def log(username, log_id):
    user = User.query.filter_by(username=username).first_or_404()
    log = user.logs.filter_by(log_id=log_id).first_or_404()
    return render_template(
        'log.html',
        user=user,
        log=log
    )

@app.route('/<string:username>/logs/add')
def addLog(username):
    user = User.query.filter_by(username = username).first_or_404()

    return render_template(
        'log.html',
        user=user,
        log=log
    )

@app.route('/<string:username>/setting')
@app.route('/<string:username>/setting/admin')
def admin(username):
    user = User.query.filter_by(username = username).first_or_404()

    return render_template(
        'admin.html',
        user = user
    )

@app.route('/<string:username>/setting/change_password', methods=['GET','POST'])
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

@app.route('/<string:username>/setting/change_username')
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




@app.route('/')
def home():
    return render_template(
        'home.html'
    )

if __name__ == '__main__':
    app.run()
