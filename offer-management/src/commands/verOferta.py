from .baseCommand import BaseCommand
from ..models.offer import Offer, OfferSchema
from flask import request, jsonify
from ..errors.errors import TokenInvalid, TokenMissing, InvalidFormat, OfferNotFound
from ..utils.valid_uuid import is_valid_uuid


class ViewOfferCommand(BaseCommand):
    def __init__(self, offer_id):
        self.offer_id = offer_id

    def execute(self):
        token = request.headers.get("Authorization").split(' ')[1] if request.headers.get('Authorization') else None
        if not token:
            raise TokenMissing()
        
        if not is_valid_uuid(token):
            raise TokenInvalid()


        if not isinstance(self.offer_id, str) or not is_valid_uuid(self.offer_id):
            raise InvalidFormat()

        query = Offer.query
        offer = query.filter_by(id=self.offer_id).first()

        if not offer:
            raise OfferNotFound()

        offer_schema = OfferSchema()
        serialized_offer = offer_schema.dump(offer)

        return jsonify(serialized_offer)

