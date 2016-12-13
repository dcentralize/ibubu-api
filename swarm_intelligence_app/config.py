import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
    SI_GOOGLE_CLIENT_ID = os.environ.get('SI_GOOGLE_CLIENT_ID')
    SI_JWT_SECRET = os.environ.get('SI_JWT_SECRET')
    SI_JWT_EXPIRATION = os.environ.get('SI_JWT_EXPIRATION') or 86400


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        'mysql+pymysql://root@localhost:3306/swarm_intelligence'


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
