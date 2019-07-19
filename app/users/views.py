from http import HTTPStatus
from flask import jsonify
from flask import make_response
from app.users.models import Users, UsersSchema
from sqlalchemy.exc import SQLAlchemyError
from flask_restplus import Api, Namespace, fields, reqparse, Resource
from app.constants import STATUS_CODE
from app.constants import GET, POST, PATCH, DELETE
from app.users.models import Post, PostSchema
from app.api.database import DB

API = Api(title='Board API',
        version='1.0',
        description="Board REST API"
        # All API metadatas
    )

SCHEMA = UsersSchema()
post_schema = PostSchema()

USER_FIELDS = API.model('Users', {
    'name': fields.String,
    'email': fields.String,
    'password': fields.String
})
POST_FIELDS = API.model('Post', {
    'name': fields.String,
    'author_id': fields.Integer,
})


@API.route('/users/<int:user_id>')
@API.param('user_id', 'The user identifier')
class UserItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, help="user's name", location='json')
    parser.add_argument('email', required=True, type=str, help="user's email", location='json')
    parser.add_argument('password', required=True, type=str, help="password", location='json')

    @API.doc(responses=GET)
    def get(self, user_id):
        user = Users.query.get_or_404(user_id)
        user = SCHEMA.dump(user).data
        return user

    @API.expect(USER_FIELDS)
    @API.doc(responses=PATCH)
    def patch(self, user_id):
        args = self.parser.parse_args()
        user = Users.query.get_or_404(user_id)
        response = user.update(args, SCHEMA)
        return response

    @API.doc(responses=DELETE)
    def delete(self, user_id):
        #import pdb; pdb.set_trace()
        user = Users.query.get_or_404(user_id)
        response = user.delete(user, SCHEMA)
        return response


@API.route('/users')
class UsersList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, help="user's name", location='json')
    parser.add_argument('email', required=True, type=str, help="user's email", location='json')
    parser.add_argument('password', required=True, type=str, help="password", location='json')

    def get(self):
        users_query = Users.query.all()
        results = SCHEMA.dump(users_query, many=True).data
        return results

    @API.expect(USER_FIELDS)
    def post(self):
        args = self.parser.parse_args()
        user = Users(args['name'], args['email'], args['password'])
        try:
            DB.session.add(user)
            DB.session.commit()
            body = jsonify({"users": SCHEMA.dump(user).data})
            code = HTTPStatus.OK
        except SQLAlchemyError as err:
            DB.session.rollback()
            message = str(err)
            body = jsonify({"message": message})
            code = HTTPStatus.INTERNAL_SERVER_ERROR
        return make_response(body, code.value)

@API.route('/posts')
class Posts(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, help="post's name", location='json')
    parser.add_argument('author_id', required=True, type=int, help="post's author", location='json')

    @API.expect(POST_FIELDS)
    def post(self):
        args_ = self.parser.parse_args()
        post = Post(name=args_['name'], author_id=args_['author_id'])
        try:
            DB.session.add(post)
            DB.session.commit()
            body = jsonify({"posts": post_schema.dump(post).data})
            code = HTTPStatus.OK
        except SQLAlchemyError as err:
            DB.session.rollback()
            message = str(err)
            body = jsonify({"message": message})
            code = HTTPStatus.INTERNAL_SERVER_ERROR
        return make_response(body, code.value)

@API.route('/post/<int:seqno>')
class PostItem(Resource):
    def get(self, seqno):
        try:
            post_item = DB.session.query(Post).outerjoin(Users, Users.id==Post.author_id).filter(Post.id==seqno).first()
            body = jsonify({"post":post_schema.dump(post_item).data})
            if post_item:
                code = HTTPStatus.OK
            else:
                code = HTTPStatus.NOT_FOUND
        except SQLAlchemyError as err:
            message = str(err)
            body = jsonify({"message": message})
            code = HTTPStatus.INTERNAL_SERVER_ERROR
        return make_response(body, code.value)

@API.route('/userLogin')
class GetUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, help="user's name", location='json')
    parser.add_argument('password', required=True, type=str, help="user's password", location='json')

    @API.expect(USER_FIELDS)
    def post(self):
        args = self.parser.parse_args()
        user = Users.query.filter(Users.name == args['name']).first()
        import pdb; pdb.set_trace()