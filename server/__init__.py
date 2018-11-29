from flask import Flask, render_template
from server.models import db
from server.extensions import bcrypt
from server.controllers.user import user_blueprint
from server.controllers.log import logs_blueprint
from server.controllers.setting import setting_blueprint


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    db.init_app(app)

    @app.route('/')
    def home():
        return render_template(
            'home.html'
        )
    app.register_blueprint(setting_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(logs_blueprint)
    
    return app
