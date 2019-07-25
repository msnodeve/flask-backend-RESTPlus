"""
    Posts view file
"""

from flask_restplus import Namespace, Resource, reqparse, fields
from flask import jsonify, make_response
from http import HTTPStatus
from sqlalchemy.exc import SQLAlchemyError
from app.posts.models import Posts, PostsSchema
from app.users.models import Users, UsersSchema
from app.api.database import DB
from app.api.auth_type import confirm_token, ACCESS_TOKEN, BASIC_AUTH

API = Namespace('Posts', description="Post's REST API")
POSTS_SCHEMA = PostsSchema()

@API.route('s')
class Post(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('author_id', required=True, type=str, help="Post's author ID", location='json')
    parser.add_argument('title', required=True, type=str, help="Post's title", location='json')
    parser.add_argument('body', required=True, type=str, help="Post's body", location='json')

    post_field = API.model('Post', {
        'author_id': fields.String,
        'title': fields.String,
        'body': fields.String
    })

    @API.doc('get')
    def get(self):
        try:
            posts = Posts.query.all()
            body = jsonify(POSTS_SCHEMA.dump(posts, many=True).data)
            if posts:
                code = HTTPStatus.OK
            else:
                code = HTTPStatus.NOT_FOUND
        except SQLAlchemyError as err:
            body = jsonify({'message' : str(err)})
            code = HTTPStatus.INTERNAL_SERVER_ERROR
        return make_response(body, code.value)

    @API.expect(post_field)
    @confirm_token
    @API.doc('post', security=ACCESS_TOKEN)
    def post(self):
        args_ = self.parser.parse_args()
        post = Posts(author_id=args_['author_id'], title=args_['title'], body=args_['body'])
        return post.add(post, POSTS_SCHEMA)

@API.route('/<int:reqno>')
class PostItem(Resource):
    @confirm_token
    @API.doc('get', security=ACCESS_TOKEN)
    def get(self, reqno):
        try:
            post = DB.session.query(Posts).outerjoin(
                Users, Users.user_id == Posts.author_id).filter(Posts.id==reqno).first()
            body = POSTS_SCHEMA.dump(post).data
            if post:
                code = HTTPStatus.OK
            else:
                code = HTTPStatus.NOT_FOUND
        except SQLAlchemyError as err:
            body = jsonify({'message' : str(err)})
            code = HTTPStatus.INTERNAL_SERVER_ERROR
        return make_response(body, code.value)