
class Config(object):
    SECRET_KEY = '5a3c5c5d31034b80e35ad114ad5114b6'

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

