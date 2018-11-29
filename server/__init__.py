
from flask import Flask, render_template
from server.config import DevConfig
from server.models import db
from server.controllers.user import user_blueprint
from server.controllers.log import logs_blueprint
from server.controllers.setting import setting_blueprint


app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)




@app.route('/')
def home():
    return render_template(
        'home.html'
    )
app.register_blueprint(setting_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(logs_blueprint)

if __name__ == '__main__':
    app.run()
