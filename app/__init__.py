"""
    app init
"""

from flask import Flask, render_template, jsonify
from flask_restplus import Resource, Api, fields, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from flask_marshmallow import Marshmallow

DB = SQLAlchemy()
SQLALCHEMY_DATABASE_URI = \
    ("mysql+pymysql://{USER}:{PASSWORD}@{ADDR}:{PORT}/{NAME}?charset=utf8")
# API Doc에 대한 설명을 덧 붙이기 위한 생성자
API = Api(version='1.0', title='Board API',
    description='A simple Board RESTPlus API',)
# 설명할 API에 대한 것
api_ns = API.namespace('userinfo', description='UserInfo operations')
MA = Marshmallow()

class UserInfo(DB.Model):
    """ UserInfo model """
    __tablename__ = "userinfo"
    __table_args__ = {'mysql_collate' : 'utf8_general_ci'}
    id = DB.Column("id", DB.Integer, primary_key=True)
    name = DB.Column("name", DB.String(250), nullable=False)
    age = DB.Column("age", DB.Integer, nullable=False)
    tel = DB.Column("tel", DB.String(20), nullable=False)
    email = DB.Column("email", DB.String(50), nullable=False)
    created = DB.Column(DB.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)

    def __init__(self, name, age, tel, email):
        self.name = name
        self.age = age
        self.tel = tel
        self.email = email

def create_app() -> (Flask):
    """ create_app() 함수를 호출해 앱을 초기화 """



    """ app config part """
    # 나중에 config는 다 빼야 할 것 같다.
    app = Flask(__name__)
    app.app_context().push()
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI.format(
        USER="root",
        PASSWORD="1234",
        ADDR="127.0.0.1",
        PORT=3306,
        NAME="board"
    )
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['DEBUG'] = True
    DB.init_app(app)
    API.init_app(app)
    MA.init_app(app)

    """ API model을 보이기 위한 설명 추가 """
    # 나중에 따로 빼야 할 것 같다.
    user_info = API.model('UserInfo', {
        'name' : fields.String(required=True, description="User's name"),
        'age' : fields.Integer(required=True, description="User's age"),
        'tel' : fields.String(required=True, description="User's tel"),
        'email' : fields.String(required=True, description="User's email")
    })

    class UserSchema(MA.Schema):
        class Meta:
            # Fields to expose
            fields = ("name", "age", "tel", "email")



    """ API.route part"""
    @api_ns.route("/hello")
    class HelloWorld(Resource):
        def get(self):
            return {'hello': 'world'}

    @api_ns.route('/users')
    class Show(Resource):
        post_parser = reqparse.RequestParser(bundle_errors=True)
        post_parser.add_argument('name', required=True, type=str, help="user name",location='json')
        post_parser.add_argument('age', required=True, type=int, help="user age",location='json')
        post_parser.add_argument('tel', required=True, type=str, help="user tel",location='json')
        post_parser.add_argument('email', required=True, type=str, help="user email",location='json')
        def get(self):
            user_schema = UserSchema(many=True)
            all_users = DB.session.query(UserInfo).all()
            result = user_schema.dump(all_users)
            return jsonify(result.data)

        @api_ns.expect(user_info)
        def post(self):
            args_ = self.post_parser.parse_args()
            user = UserInfo(name=args_['name'], age=args_['age'], tel=args_['tel'], email=args_['email'])
            message = "not working"
            try:
                DB.session.add(user)
                DB.session.commit()
                message = "success"
            except SQLAlchemyError as err:
                message = str(err)
                DB.session.rollback()
            finally:
                DB.session.close()
            return message

        @api_ns.expect(user_info)
        def delete(self):
            args_ = self.post_parser.parse_args()
            user = UserInfo.query.filter_by(name=args_['name']).first()
            try:
                DB.session.delete(user)
                DB.session.commit()
                message = "success"
            except SQLAlchemyError as err:
                message = str(err)
                DB.session.rollback()
            finally:
                DB.session.close()
            return message

    @api_ns.route('/test')
    class Test(Resource):
        post_parser = reqparse.RequestParser(bundle_errors=True)
        post_parser.add_argument('name', required=True, type=str, help="user name",location='json')
        post_parser.add_argument('age', required=True, type=int, help="user age",location='json')
        post_parser.add_argument('tel', required=True, type=str, help="user tel",location='json')
        post_parser.add_argument('email', required=True, type=str, help="user email",location='json')
        def get(self):
            return {'test' : 'test'}
        
        @api_ns.expect(user_info)
        def post(self):
            args_ = self.post_parser.parse_args()
            user = UserInfo(name=args_['name'], age=args_['age'], tel=args_['tel'], email=args_['email'])
            return {'name' : 'server' + user.name, 'age' : user.age, 'tel' : user.tel, 'email' : user.email}


    @api_ns.route('/test')
    class HelloWorld(Resource):
        post_parser = reqparse.RequestParser(bundle_errors=True)
        post_parser.add_argument('name', required=True, type=str, help="user name",location='json')
        post_parser.add_argument('tel', type=str, help="user tel",location='json')

        def get(self):
            userInfo = DB.session.query(UserInfo).all()
            import pdb; pdb.set_trace()
            return {'hello': 'world'}

        @api_ns.expect(user_info)
        def post(self):
            """ 유저 생성 """
            args_ = self.post_parser.parse_args()
            user = UserInfo(name=args_['name'], tel=args_['tel'])
            message = "not working"
            try:
                DB.session.add(user)
                DB.session.commit()
                message = "success"
            except SQLAlchemyError as err:
                message = str(err)
                DB.session.rollback()
            finally:
                DB.session.close()
            return message

    """ return part """
    return app