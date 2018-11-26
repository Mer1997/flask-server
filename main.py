from flask import Flask
from config import DevConfig

app = Flask(__name__)
app.config.from_object(Devconfig)

@app.route('/')
def home():
    return '<h1>Hello World<h1>'

if __name__ == '__main__':
    app.run()
