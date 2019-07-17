from flask import jsonify
from flask import make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from app.constants import STATUS_CODE
from flask_restplus import reqparse

DB = SQLAlchemy()

class CRUD:
    body = ''
    status_code = STATUS_CODE.NOT_IMPLEMENTED
    def add(self, resource, schema):
        try:
            DB.session.add(resource)
            DB.session.commit()
            query = resource.query.get(resource.id)
            self.body = jsonify(schema.dump(resource).data)
            self.status_code = STATUS_CODE.CREATED
        except IntegrityError as error:
            DB.session.rollback()
            error_message = str(error)
            self.body = jsonify({"error": error_message, "type":"IntegrityError"})
            if "Duplicate entry" in error_message:
                self.status_code = 404
            else:
                self.status_code = 400
        finally:
            response = (self.body, self.status_code.value)
            response = make_response(response)
            
        return response 

    def update(self, args, schema):
        try:
            for key, value in args.items():
                setattr(self, key, value)
            DB.session.commit()
            self.body = jsonify(schema.dump(self).data)
            self.status_code = STATUS_CODE.OK
        except IntegrityError as error:
            DB.session.rollback()
            error_message = str(error) 
            self.body = jsonify({"error": error_message, "type":"IntegrityError"})
            if "Duplicate entry" in error_message:
                self.status_code = STATUS_CODE.CONFLICT
            else:
                self.status_code = STATUS_CODE.BAD_REQUEST
        finally:
            response = (self.body, self.status_code.value)
            response = make_response(response)
        return response

    def delete(self, resource, schema):
        DB.session.delete(resource)
        DB.session.commit()
        self.body = jsonify({"message":"success"})
        self.status_code = STATUS_CODE.OK
        response = (self.body, self.status_code.value)
        response = make_response(response)
        return response
