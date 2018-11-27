from flask import Flask, render_template
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy, func

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
        return "<Log '{}'>".format(self.info)


@app.route('/user/<string:username>')
def get_info(username):
    user = User.query.filter_by(username = username).first_or_404()
    
    return render_template(
            'user.html'
            user = user
    )

@app.route('/log/<string:username>')
def get_logs(username):
    user = User.query.filter_by(username = username).first_or_404()
    logs = user.logs.order_by(Logs.created.desc()).all()

    return render_template(
        'logs.html',
        user=user,
        logs=logs
    )



@app.route('/')
def home():
    return '<h1>Hello World<h1>'

if __name__ == '__main__':
    app.run()
