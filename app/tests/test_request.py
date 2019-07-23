from http import HTTPStatus
from app import create_app

def test_url(flask_app):
    with flask_app.test_client() as client:
        response = client.get('/posts')
        assert response.status_code == HTTPStatus.OK