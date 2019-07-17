from app.users.models import Users, UsersSchema
from flask_restplus import Api, Namespace, fields, reqparse, Resource
from app.constants import STATUS_CODE
from app.constants import GET, POST, PATCH, DELETE

API = Api(title='users',
          version='1.0',
          description="User's REST API"
          # All API metadatas
          )

SCHEMA = UsersSchema()

USER_FIELDS = API.model('Users', {
	'name': fields.String,
	'email': fields.String,
	'password': fields.String
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
		response = user.add(user, SCHEMA)
		return response
