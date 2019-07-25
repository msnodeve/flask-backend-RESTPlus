"""
    Create db
"""
from flask import jsonify
from flask import make_response
from http import HTTPStatus
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_marshmallow import Marshmallow

DB = SQLAlchemy()
MA = Marshmallow()

class CRUD:
    body = ''
    status_code = HTTPStatus.NOT_IMPLEMENTED

    def add(self, resource, schema):
        try:
            DB.session.add(resource)
            DB.session.commit()
            self.body = jsonify(schema.dump(resource).data)
            self.status_code = HTTPStatus.OK
        except IntegrityError as err:
            DB.session.rollback()
            err_meg = str(err)
            self.body = jsonify({'error' : err_meg, 'type' : 'IntegrityError'})
            if "Duplicate entry" in err_meg:
                self.status_code = HTTPStatus.CONFLICT
            else:
                self.status_code = HTTPStatus.BAD_REQUEST
        return make_response(self.body, self.status_code)
    