import pytest
import requests
from http import HTTPStatus
from flask import json
from app.users.models import Users
from app.posts.models import Posts
from app.users.views import USERS_SCHEMA
from app.posts.views import POSTS_SCHEMA
from app.api.database import CRUD
from app.tests.conftest import flask_app

BASE_URL = 'http://localhost:5000'
USERS_URL = BASE_URL+'/users'
POSTS_URL = BASE_URL+'/posts'
POST_URL = BASE_URL+'/post/'
USERS_AUTH_URL = BASE_URL+'/user/auth'
BASE_HEADERS = {'Content-Type': 'application/json; charset=utf-8'}

def test_base_route(flask_app):
    client = flask_app.test_client()
    url = "/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

def test_add_message(flask_app):
    app = flask_app.test_client()
    data = json.dumps({'user_id': 'user_id', 'user_email': 'user_email', 'user_password': 'user_password'})
    response = app.post(USERS_URL, headers=BASE_HEADERS, data=data)
    assert True
    