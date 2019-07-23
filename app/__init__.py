"""
    APP을 실행하기 위해 config file
"""

from flask import Flask
from app.api.database import DB, MA
from app.api import REST_API
from app.constants import SQLALCHEMY_DATABASE_URI_FORMAT


def create_app()->(Flask):
    """ create_app()을 호출하여 app을 초기화 """
    app = Flask(__name__)
    app.app_context().push()
    
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_FORMAT
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['DEBUG'] = True

    DB.init_app(app)
    REST_API.init_app(app)
    MA.init_app(app)
    
    return app
