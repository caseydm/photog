import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # stormpath config
    STORMPATH_API_KEY_ID = os.environ.get('STORMPATH_API_KEY_ID')
    STORMPATH_API_KEY_SECRET = os.environ.get('STORMPATH_API_KEY_SECRET')
    STORMPATH_APPLICATION = 'photog'

    STORMPATH_REDIRECT_URL = '/dashboard'
    STORMPATH_ENABLE_REGISTRATION = False
    STORMPATH_LOGIN_TEMPLATE = 'account/login.html'
    STORMPATH_ENABLE_FORGOT_PASSWORD = True
    STORMPATH_FORGOT_PASSWORD_TEMPLATE = 'account/forgot.html'
    STORMPATH_FORGOT_PASSWORD_EMAIL_SENT_TEMPLATE = 'account/forgot_email_sent.html'
    STORMPATH_FORGOT_PASSWORD_CHANGE_TEMPLATE = 'account/forgot_change.html'
    STORMPATH_FORGOT_PASSWORD_COMPLETE_TEMPLATE = 'account/forgot_complete.html'

    # database
    SQLALCHEMY_DATABASE_URI = ""

    # sendgrid
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    # database
    SQLALCHEMY_DATABASE_URI = ""


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ""
    STORMPATH_APPLICATION = 'photog_test'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ""
    STORMPATH_APPLICATION = 'photog'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
