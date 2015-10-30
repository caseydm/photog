from flask import Flask
from flask.ext.stormpath import StormpathManager
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

stormpath_manager = StormpathManager()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    stormpath_manager.init_app(app)
    db.init_app(app)

    # register blueprints
    from .accounts import accounts as accounts_blueprint
    app.register_blueprint(accounts_blueprint)
    from .dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)
    from .public import public as public_blueprint
    app.register_blueprint(public_blueprint)

    return app
