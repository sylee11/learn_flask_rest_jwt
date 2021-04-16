import os

if os.path.exists('config.env'):
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


class Config(object):
    APP_NAME = os.getenv('APP_NAME', 'flask_restful')
    SECRET_KEY = os.getenv('SECRET_KEY', '12312312312312')
    print('secret_key', SECRET_KEY)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:Anhkuteo12345@' \
                              'localhost/flask_base'


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''


config = {
    'development' : DevelopmentConfig,
    'production' : ProductionConfig
}