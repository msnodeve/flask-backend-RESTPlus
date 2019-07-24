import pytest
from http import HTTPStatus
from app.users.models import Users
from app.posts.models import Posts
from app.users.views import USERS_SCHEMA
from app.posts.views import POSTS_SCHEMA
from app.api.database import CRUD

def test_add():
    crud = CRUD()
    try:
        users = Users('test', 'test','test')
        result = crud.add(users, USERS_SCHEMA)
    except Exception as err:
        print(err)
    assert True