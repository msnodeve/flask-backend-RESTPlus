"""
    User views file
"""
import jwt
import bcrypt
from http import HTTPStatus
from flask import jsonify, make_response
from sqlalchemy.exc import SQLAlchemyError
from flask_restplus import Namespace, Resource, reqparse, fields
from app.users.models import Users, UsersSchema
from app.api.database import DB
from app.api.auth_type import SECERET_KEY

API = Namespace('Users', description="User's RESTPlus - API")
USERS_SCHEMA = UsersSchema()


@API.route('s')
class UsersAuth(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True, type=str,
                        help="User's ID", location='json')
    parser.add_argument('user_password', required=True,
                        type=str, help="User's PW", location='json')
    parser.add_argument('user_email', required=True, type=str,
                        help="User's Email", location='json')

    users_field = API.model('userRegister', {
        'user_id': fields.String,
        'user_password': fields.String,
        'user_email': fields.String
    })

    @API.doc('post')
    @API.expect(users_field)
    def post(self):
        args_ = self.parser.parse_args()
        password = args_['user_password']
        hash_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = Users(args_['user_id'], hash_pw, args_['user_email'])
        return user.add(user, USERS_SCHEMA)


@API.route('/auth')
class UserAuth(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True, type=str,
                        help="User's ID", location='json')
    parser.add_argument('user_password', required=True,
                        type=str, help="User's PW", location='json')

    user_login_field = API.model('userLogin', {
        'user_id': fields.String,
        'user_password': fields.String
    })

    @API.doc('post')
    @API.expect(user_login_field)
    def post(self):
        args_ = self.parser.parse_args()
        try:
            user = Users.query.filter(Users.user_id == args_['user_id']).first()
            if bcrypt.checkpw(args_['user_password'].encode('utf-8'), user.user_password.encode('utf-8')):
                # token 발급
                payload = {
                    'user_id' : user.user_id
                }
                token = jwt.encode(payload, SECERET_KEY, "HS256")
                body = jsonify({'access_token': token.decode('utf-8'),'user': user.id})
            if user:
                code = HTTPStatus.OK
            else:
                code = HTTPStatus.NOT_FOUND
        except SQLAlchemyError as err:
            body = jsonify({'message': str(err)})
            code = HTTPStatus.INTERNAL_SERVER_ERROR
        return make_response(body, code.value)
