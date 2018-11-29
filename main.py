from flask import Flask, render_template
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

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

@app.route('/<string:username>/setting/change_password')
def changePassword(username):
    pass

@app.route('/<string:username>/setting/change_username')
def changeUsername(username):
    pass




@app.route('/')
def home():
    return render_template(
        'home.html'
    )

if __name__ == '__main__':
    app.run()
