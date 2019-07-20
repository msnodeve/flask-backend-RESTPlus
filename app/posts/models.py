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
    name = DB.Column(DB.String(255), nullable=False)
    author_id = DB.Column(DB.Integer, DB.ForeignKey(Users.id))
    author = DB.relationship("Users", uselist=False)

    def __init__(self, name: str, author_id: int):
        self.name = name
        self.author_id = author_id

class PostSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    author = fields.Nested(UsersSchema)
