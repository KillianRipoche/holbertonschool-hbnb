import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    ADMIN_SECRET = os.getenv('ADMIN_SECRET', 'default_admin_secret')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
