from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

