"""
    app init
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

DB = SQLAlchemy()
SQLALCHEMY_DATABASE_URI = \
    ("mysql+pymysql://{USER}:{PASSWORD}@{ADDR}:{PORT}/{NAME}?charset=utf8")

class Userinfo(DB.Model):
    """ Userinfo model """
    __tablename__ = "userinfo"
    __table_args__ = {'mysql_collate' : 'utf8_general_ci'}
    id = DB.Column("id", DB.Integer, primary_key=True)
    name = DB.Column("name", DB.String(250), nullable=False)
    tel = DB.Column("tel", DB.String(20), nullable=False)
    created = DB.Column(DB.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)

    def __init__(self, name, tel):
        self.name = name
        self.tel = tel

def create_app() -> (Flask):
    """ create_app() 함수를 호출해 앱을 초기화 """

    """ app config part """
    # 나중에 config는 다 빼야 할 것 같다.
    app = Flask(__name__)
    app.app_context().push()
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI.format(
        USER="root",
        PASSWORD="1234",
        ADDR="127.0.0.1",
        PORT=3306,
        NAME="board"
    )
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['DEBUG'] = True
    DB.init_app(app)

    """ route part """
    # 나중에 route는 다 빼야 할 것 같다.
    @app.route("/")
    def index():
        """ / url index """
        return "<h1>Hello World ! <br> This is index page</h1>"
    
    """ return part """
    return app