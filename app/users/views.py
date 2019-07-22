
import jwt
import datetime
import bcrypt
from http import HTTPStatus
from flask import jsonify
from flask import make_response
from flask import request
from app.users.models import Users, UsersSchema
from sqlalchemy.exc import SQLAlchemyError
from flask_restplus import Api, Namespace, fields, reqparse, Resource
from app.constants import STATUS_CODE
from app.constants import GET, POST, PATCH, DELETE
from app.api.database import DB
from app.api.auth_type import BASIC_AUTH, ACCESS_TOKEN, SECERET_KEY
from app.api.auth_type import login_required

API = Namespace('Users', description="User's REST API")

USERS_SCHEMA = UsersSchema()


@API.route('/<int:user_id>')
@API.param('user_id', 'The user identifier')
class UserItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str,
                        help="user's name", location='json')
    parser.add_argument('email', required=True, type=str,
                        help="user's email", location='json')
    parser.add_argument('password', required=True, type=str,
                        help="password", location='json')

    user_field = API.model('Users', {
        'name': fields.String,
        'email': fields.String,
        'password': fields.String
    })

    @API.doc(responses=GET)
    def get(self, user_id):
        user = Users.query.get_or_404(user_id)
        Users.session.close()
        user = USERS_SCHEMA.dump(user).data
        return user

    @API.expect(user_field)
    @API.doc(responses=PATCH)
    def patch(self, user_id):
        args = self.parser.parse_args()
        user = Users.query.get_or_404(user_id)
        response = user.update(args, USERS_SCHEMA)
        return response

    @API.doc(responses=DELETE)
    def delete(self, user_id):
        #import pdb; pdb.set_trace()
        user = Users.query.get_or_404(user_id)
        response = user.delete(user, USERS_SCHEMA)
        return response


@API.route('s')
class UsersList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str,
                        help="user's name", location='json')
    parser.add_argument('email', required=True, type=str,
                        help="user's email", location='json')
    parser.add_argument('password', required=True, type=str,
                        help="password", location='json')

    user_field = API.model('Users', {
        'name': fields.String,
        'email': fields.String,
        'password': fields.String
    })
    @API.doc(responses=GET, security=ACCESS_TOKEN)
    @login_required
    def get(self):
        users_query = Users.query.all()
        results = USERS_SCHEMA.dump(users_query, many=True).data
        return results

    @API.expect(user_field)
    def post(self):
        args = self.parser.parse_args()
        temp = args['password']
        hash_pw = bcrypt.hashpw(temp.encode(), bcrypt.gensalt())
        t1 = bcrypt.checkpw(temp.encode(), hash_pw)
        user = Users(args['name'], args['email'], hash_pw)
        try:
            DB.session.add(user)
            DB.session.commit()
            body = jsonify({"users": USERS_SCHEMA.dump(user).data})
            code = HTTPStatus.OK
        except SQLAlchemyError as err:
            DB.session.rollback()
            message = str(err)
            body = jsonify({"message": message})
            code = HTTPStatus.INTERNAL_SERVER_ERROR
        return make_response(body, code.value)


@API.route('/auth')
class GetUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str,
                        help="user's name", location='json')
    parser.add_argument('password', required=True, type=str,
                        help="user's password", location='json')

    user_field = API.model('Auth', {
        'name': fields.String,
        'password': fields.String
    })

    @API.doc(responses=POST)
    @API.expect(user_field)
    def post(self):
        args = self.parser.parse_args()
        try:
            user = Users.query.filter(Users.name == args['name']).first()
            if bcrypt.checkpw(args['password'].encode('utf-8'), user.password.encode('utf-8')):
                #여기서 이제 토큰 발급해서 보내주기
                payload = {
                    'user_id' : user.name
                }
                token = jwt.encode(payload, SECERET_KEY, "HS256")
                body = jsonify({"access_token": token.decode('utf-8'), "user": {"id" : user.id}})
            if user:
                code = HTTPStatus.OK
            else:
                code = HTTPStatus.NOT_FOUND
        except SQLAlchemyError as err:
            message = str(err)
            body = jsonify({"message": message})
            code = HTTPStatus.INTERNAL_SERVER_ERROR
        return make_response(body, code.value)
