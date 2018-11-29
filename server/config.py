from os import path

class Config(object):
    SECRET_KEY = '5a3c5c5d31034b80e35ad114ad5114b6'
    RECAPTCHA_PUBLIC_KEY="6Ld03n0UAAAAAE9966lZhkOUbrvYnGN9aL1_NsGX"
    RECAPTCHA_PRIVATE_KEY="6Ld03n0UAAAAAPWMuDAHp759Eggi6rsgVyg5RY57"

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI='sqlite:///'+path.join(path.abspath(path.pardir),'database.db')
    DEBUG=True

class ProdConfig(Config):
    pass
