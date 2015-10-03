from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

from views import app, db

# app conig
app.config.from_object('config')
app.config.from_pyfile('config.py')

# database migration setup
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
