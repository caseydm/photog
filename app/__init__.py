from flask import Flask
from flask.ext.stormpath import StormpathManager

# app setup
app = Flask(__name__, instance_relative_config=True)

# app conig
app.config.from_object('config')
app.config.from_pyfile('config.py')

# stormpath setup
stormpath_manager = StormpathManager(app)

# Register blueprint(s)
from app.accounts.views import mod as accounts
app.register_blueprint(accounts)
