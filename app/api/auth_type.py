from flask import request
from functools import wraps
import jwt

SECERET_KEY = "Hello"
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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers['Authorization']
        if access_token is not None:
            try:
                payload = jwt.decode(access_token, SECERET_KEY, "HS256")
            except jwt.InvalidTokenError:
                payload = None

            # if payload is None:
            #     return Response(status=401)

            user_id = payload["user_id"]
            # g.user = get_user_info(user_id) if user_id else None
        else:
            return Response(status=401)

        return f(*args, **kwargs)
    return decorated_function