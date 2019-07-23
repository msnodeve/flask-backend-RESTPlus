"""
    Posts model file
"""

from app.api.database import DB, MA, CRUD
from marshmallow import Schema, fields, validate
from app.users.models import Users, UsersSchema
from sqlalchemy.sql import text

class Posts(DB.Model, CRUD):
    __tablename__ = 'posts'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = DB.Column(DB.Integer, primary_key=True)
    author_id = DB.Column(DB.String(255), DB.ForeignKey(Users.user_id))
    title = DB.Column(DB.String(512), nullable=False)
    body = DB.Column(DB.String(1024), nullable=False)
    author = DB.relationship('Users', uselist=False)
    created = DB.Column(DB.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)

    def __init__(self, author_id, title, body):
        self.author_id = author_id
        self.title = title
        self.body = body

class PostsSchema(MA.Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer()
    author_id = fields.String(validate=not_blank)
    title = fields.String(validate=not_blank)
    body = fields.String(validate=not_blank)
    author = fields.Nested(UsersSchema)
    created = fields.String(validate=not_blank)
