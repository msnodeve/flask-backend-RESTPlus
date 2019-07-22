from typing import Callable
from functools import wraps
from app import create_app
from flask import current_app
from flask import request
from datetime import timezone, timedelta, datetime
import jwt

encoded_jwt = jwt.encode({'exp': datetime.utcnow()}, 'secret', algorithm='HS256')

class UnAuthorizeError(Exception):
    """ 인증 실패 """

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization = request.headers['Authorization']
        if authorization != 'token': # db or jwt.decode
            raise UnAuthorizeError("인증이 필요합니다")
        return f(*args, **kwargs)
    return decorated

@requires_auth
def something(*args, **kwargs):
    # import pdb;pdb.set_trace()
    return args, kwargs

def test_decorator(flask_app):
    with flask_app.test_request_context(headers={"Authorization":"adsf"}):
        try:
            result = something()
            assert False
        except UnAuthorizeError as err:
            message = str(err)
            print(message)
