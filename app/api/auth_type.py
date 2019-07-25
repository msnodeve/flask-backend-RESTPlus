import jwt
from flask import request, Response
from functools import wraps

SECERET_KEY = "Secret Hellow"
ACCESS_TOKEN = {
    'Access Token': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
BASIC_AUTH = {
	'Basic Auth': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    },
}

def confirm_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers['Authorization']
        if access_token is not None:
            try:
                payload = jwt.decode(access_token, SECERET_KEY, "HS256")
            except jwt.InvalidTokenError:
                payload = None
            if payload is None:
                return Response(status=401)
            user_id = payload["user_id"]
            # 원하는 작업
        else:
            return Response(status=401)

        return f(*args, **kwargs)
    return decorated_function