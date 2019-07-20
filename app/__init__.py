"""
    app init
"""
from flask import Flask, render_template, jsonify
from flask_restplus import Resource, Api, fields, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from flask_marshmallow import Marshmallow
from app.api.database import DB
from app.api import  REST_API

SQLALCHEMY_DATABASE_URI = \
    ("mysql+pymysql://{USER}:{PASSWORD}@{ADDR}:{PORT}/{NAME}?charset=utf8")
# 설명할 API에 대한 것
MA = Marshmallow()
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
    REST_API.init_app(app)
    MA.init_app(app)

    """ return part """
    return app
