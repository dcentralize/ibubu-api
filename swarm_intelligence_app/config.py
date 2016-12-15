"""
Define classes for app configuration.

"""
import os


class Config:
    """
    Define base configuration.
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
    SI_GOOGLE_CLIENT_ID = os.environ.get('SI_GOOGLE_CLIENT_ID')
    SI_JWT_SECRET = os.environ.get('SI_JWT_SECRET') or 'top_secret'
    SI_JWT_EXPIRATION = os.environ.get('SI_JWT_EXPIRATION') or 86400


class DevelopmentConfig(Config):
    """
    Define development configuration.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        'mysql+pymysql://root@localhost:3306/swarm_intelligence'


class TestingConfig(Config):
    """
    Define testing configuration.
    """
    pass


class ProductionConfig(Config):
    """
    Define production configuration.
    """
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
