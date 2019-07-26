import pytest
from http import HTTPStatus
from app.tests.conftest import flask_app

@pytest.fixture(scope='session')
def test_base_route(flask_app):
    client = flask_app.test_client()
    url = "/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK