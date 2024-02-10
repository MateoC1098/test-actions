from .baseCommand import BaseCommand
from ..models import Offer, db
from flask import request, jsonify
from ..errors.errors import TokenInvalid, TokenMissing, FieldsMissing, InvalidFormat, InvalidValues, OfferCreationSuccess
from ..utils.valid_uuid import is_valid_uuid
from ..utils.check_token import check_token
import os

class CreateOfferCommand(BaseCommand):
  
    def __init__(self, data):
        self.data = data

    def execute(self):
        
        token = request.headers.get("Authorization").split(' ')[1] if request.headers.get('Authorization') else None
        check_token(token)
        userId = token
        
        if not token:
            raise TokenMissing()
        
        if not is_valid_uuid(token):
            raise TokenInvalid()
                
        postId = self.data.get("postId")
        if postId is None or postId.strip() == '':
            raise FieldsMissing()
        else:
            if not is_valid_uuid(postId):
                raise InvalidFormat
        
        description = self.data.get("description")
        size = self.data.get("size")
        fragile = self.data.get("fragile")
        offer = self.data.get("offer")
        
        # Validar que todos los campos estén presentes
        if not all([postId, description, size, offer]):
            raise FieldsMissing()
        
        if fragile is None:
            raise FieldsMissing()
        
        # Validar el formato esperado de los campos
        if fragile is not None and not isinstance(fragile, bool):
            raise InvalidFormat()
        if offer is not None and not isinstance(offer, (int, float)):
            raise InvalidFormat()

        # Validar valores entre lo esperado
        if size not in ["LARGE", "MEDIUM", "SMALL"]:
            raise InvalidValues()
        elif fragile is not None and not isinstance(fragile, bool):
            raise InvalidValues()
        elif not isinstance(fragile, bool) or offer < 0:
            raise InvalidValues()

        
        # Create a new offer
        new_offer = Offer(
            postId=postId,
            userId=userId,
            description=description,
            size=size,
            fragile=fragile,
            offer=offer
        )

        db.session.add(new_offer)
        db.session.commit()
        
        offer_details = {
        "id": new_offer.id,
        "userId": new_offer.userId,
        "createdAt": new_offer.createdAt
    }

        return jsonify(offer_details), 201