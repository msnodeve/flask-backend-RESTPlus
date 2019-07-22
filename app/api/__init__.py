from flask_restplus import Api
from app.users.views import API as users_api
from app.posts.views import API as posts_api
from app.api.auth_type import ACCESS_TOKEN, BASIC_AUTH


REST_API = Api(authorizations={**ACCESS_TOKEN, **BASIC_AUTH})

REST_API.add_namespace(users_api, '/user')
REST_API.add_namespace(posts_api, '/posts')
