from app.api.database import DB, CRUD
from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from marshmallow import validate
from sqlalchemy.sql import text
from app.users.models import Users, UsersSchema

class Post(DB.Model):
    __tablename__ = 'posts'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = DB.Column(DB.Integer, primary_key=True)
    author_id = DB.Column(DB.Integer, DB.ForeignKey(Users.id))
    name = DB.Column(DB.String(255), nullable=False)
    title = DB.Column(DB.String(255), nullable=False)
    body = DB.Column(DB.String(1024), nullable=False)
    author = DB.relationship("Users", uselist=False)
    created = DB.Column(DB.TIMESTAMP, server_default=text(
        "CURRENT_TIMESTAMP"), nullable=False)

    def __init__(self, name: str, title : str, body : str, author_id: int):
        self.name = name
        self.title = title
        self.body = body
        self.author_id = author_id

class PostSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    title = fields.Str()
    body = fields.Str()
    author = fields.Nested(UsersSchema)
    created = fields.Str()
