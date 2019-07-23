"""
    Users models file
"""
from sqlalchemy.sql import text
from app.api.database import DB, MA
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate

class Users(DB.Model):
    __tablename__ = 'users'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.String(255), unique=True, nullable=False)
    user_password = DB.Column(DB.String(255), nullable=False)
    user_email = DB.Column(DB.String(255), nullable=False)
    created = DB.Column(DB.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)

    def __init__(self, user_id, user_password, user_email):
        self.user_id = user_id
        self.user_password = user_password
        self.user_email = user_email

class UsersSchema(MA.Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    user_id = fields.String(validate=not_blank)
    user_password = fields.String(validate=not_blank)
    user_email = fields.String(validate=not_blank)
    created = fields.String(validate=not_blank)