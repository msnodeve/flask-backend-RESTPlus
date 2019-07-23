"""
    APP manage file
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.api.database import DB
from app.users.models import Users, UsersSchema

APP = create_app()
MANAGER = Manager(APP)
MIGRATE = Migrate(APP, DB)
MANAGER.add_command('db', MigrateCommand)

@MANAGER.command
def run():
    """ Command Application run """
    APP.run()

if __name__ == '__main__':
    MANAGER.run()