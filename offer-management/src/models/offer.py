from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from datetime import datetime
import uuid

db = SQLAlchemy()

class Offer(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    postId = db.Column(db.String, nullable=False)
    userId = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)
    fragile = db.Column(db.Boolean, default=False, nullable=False)
    offer = db.Column(db.Float, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False )

class OfferSchema(SQLAlchemyAutoSchema):
    createdAt = fields.DateTime(format="%Y-%m-%dT%H:%M:%S")
    
    class Meta:
        model = Offer
        load_instance = True