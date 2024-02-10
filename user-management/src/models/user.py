import enum
from marshmallow import Schema, fields
from sqlalchemy import Column, String, DateTime
from .model import Model
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import uuid

db = SQLAlchemy()

class Status(enum.Enum):
    POR_VERIFICAR = 1
    NO_VERIFICADO = 2
    VERIFICADO = 3

class User(Model, db.Model):
    __tablename__ = 'user'

    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    phoneNumber = Column(String)
    dni = Column(String)
    fullName = Column(String)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    token = Column(String)
    status = Column(db.Enum(Status), nullable=False)
    expireAt = Column(DateTime)

    def __init__(self, username, email, password, salt, status, phoneNumber=None, dni=None, fullName=None, token=None, expireAt=None):
        Model.__init__(self)
        self.username = username
        self.email = email
        self.password = password
        self.salt = salt
        self.status = status
        self.phoneNumber = phoneNumber
        self.dni = dni
        self.fullName = fullName
        self.token = token
        self.expireAt = expireAt

    ## Generar token por ahora es el mismo id
    def generate_token(self):
        # Generar token
        self.token = str(uuid.uuid4())
        self.expireAt= datetime.utcnow() + timedelta(minutes=60)

class UserJsonSchema(Schema):
    id = fields.Number()
    username = fields.Str()
    email = fields.Str()
    phoneNumber = fields.Str()
    dni = fields.Str()
    fullName = fields.Str()
    password = fields.Str()
    salt = fields.Str()
    token = fields.Str()
    extension = fields.Method("get_status")
    expireAt = fields.DateTime()
    createdAt = fields.DateTime()
    updatedAt = fields.DateTime()

    def get_status(self, obj):
        return obj.status.name    