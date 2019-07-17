from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from app.constants import STATUS_CODE
from flask_restplus import reqparse