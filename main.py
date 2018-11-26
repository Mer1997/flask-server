from flask import Flask
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy

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
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime())
    info = db.Column(db.Text)
    stat = db.Column(db.Text)

    def __init__(self, info):
        self.info = info

    def __repr__(self):
        return "<Post '{}'>".format(self.info)


@app.route('/')
def home():
    return '<h1>Hello World<h1>'

if __name__ == '__main__':
    app.run()
