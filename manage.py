import os

from app import create_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host="localhost"))


@manager.command
def create_db():
    db.drop_all()


if __name__ == '__main__':
    manager.run()