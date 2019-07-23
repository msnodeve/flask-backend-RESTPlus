"""
    API config file
"""

from flask_restplus import Api
from app.users.views import API as users_api
from app.posts.views import API as posts_api

REST_API = Api()

REST_API.add_namespace(users_api, '/user')
REST_API.add_namespace(posts_api, '/post')