from http import HTTPStatus
from flask import jsonify
from flask import make_response
from app.users.models import Users, UsersSchema
from sqlalchemy.exc import SQLAlchemyError
from flask_restplus import Api, Namespace, fields, reqparse, Resource
from app.constants import STATUS_CODE
from app.constants import GET, POST, PATCH, DELETE
from app.posts.models import Post, PostSchema
from app.api.database import DB
from app.api.auth_type import login_required
from app.api.auth_type import BASIC_AUTH, ACCESS_TOKEN, SECERET_KEY

API = Namespace('Posts', description="Post's REST API")

POSTS_SCHEMA = PostSchema()

POST_FIELDS = API.model('Post', {
    'name': fields.String,
    'title': fields.String,
    'body': fields.String,
    'author_id': fields.Integer,
})

@API.route('')
class Posts(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str,
                        help="post's name", location='json')
    parser.add_argument('title', required=True, type=str,
                        help="post's title", location='json')
    parser.add_argument('body', required=True, type=str,
                        help="post's body", location='json')
    parser.add_argument('author_id', required=True, type=int,
                        help="post's author", location='json')

    @API.doc(responses=GET, security=ACCESS_TOKEN)
    @login_required
    def get(self):
        try:
            posts_query = Post.query.all()
            body = jsonify(POSTS_SCHEMA.dump(posts_query, many=True).data)
            if posts_query:
                code = HTTPStatus.OK
            else:
                code = HTTPStatus.NOT_FOUND
        except SQLAlchemyError as err:
            message = str(err)
            body = jsonify({"message": message})
            code = HTTPStatus.INTERNAL_SERVER_ERROR
        return make_response(body, code.value)

    @API.expect(POST_FIELDS)
    def post(self):
        args_ = self.parser.parse_args()
        post = Post(name=args_['name'], title=args_['title'], body=args_[
                    'body'], author_id=args_['author_id'])
        try:
            DB.session.add(post)
            DB.session.commit()
            body = jsonify({"posts": POSTS_SCHEMA.dump(post).data})
            code = HTTPStatus.OK
        except SQLAlchemyError as err:
            DB.session.rollback()
            message = str(err)
            body = jsonify({"message": message})
            code = HTTPStatus.INTERNAL_SERVER_ERROR
        return make_response(body, code.value)


@API.route('/<int:seqno>')
class PostItem(Resource):
    def get(self, seqno):
        try:
            post_item = DB.session.query(Post).outerjoin(
                Users, Users.id == Post.author_id).filter(Post.id == seqno).first()
            body = jsonify({"post": POSTS_SCHEMA.dump(post_item).data})
            if post_item:
                code = HTTPStatus.OK
            else:
                code = HTTPStatus.NOT_FOUND
        except SQLAlchemyError as err:
            message = str(err)
            body = jsonify({"message": message})
            code = HTTPStatus.INTERNAL_SERVER_ERROR
        return make_response(body, code.value)
