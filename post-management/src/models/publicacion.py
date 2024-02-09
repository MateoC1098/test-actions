from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from datetime import datetime
import uuid

db = SQLAlchemy()

class Publicacion(db.Model):

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    routeId = db.Column(db.String, nullable=False)
    userId = db.Column(db.String, nullable=False)
    expireAt = db.Column(db.DateTime, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now().isoformat(), nullable=False)


class PublicacionSchema(SQLAlchemyAutoSchema):

    expireAt = fields.DateTime(format="%Y-%m-%dT%H:%M:%S")
    createdAt = fields.DateTime(format="%Y-%m-%dT%H:%M:%S")
    class Meta:
        model = Publicacion
        load_instance = True

