from app.api.database import DB
from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from marshmallow import validate
from sqlalchemy.sql import text

class Users(DB.Model):
    __tablename__ = 'users'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(255), nullable=False)
    email = DB.Column(DB.String(50), unique=True, nullable=False)
    password = DB.Column(DB.String(255), nullable=False)
    created = DB.Column(DB.TIMESTAMP, server_default=text(
        "CURRENT_TIMESTAMP"), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password



class UsersSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    email = fields.String(validate=not_blank)
    name = fields.String(validate=not_blank)
    password = fields.String(validate=not_blank)
    created = fields.String(validate=not_blank)

    def get_top_level_links(self, data, many):
        if many:
            self_link = "/users"
        else:
            self_link = "/users/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'users'
        strict = True
