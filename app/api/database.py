"""
    Create db
"""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

DB = SQLAlchemy()
MA = Marshmallow()