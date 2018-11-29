from os import path

class Config(object):
    SECRET_KEY = '5a3c5c5d31034b80e35ad114ad5114b6'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI='sqlite:///'+path.join(path.abspath(path.pardir),'database.db')
    DEBUG=True

class ProdConfig(Config):
    pass
