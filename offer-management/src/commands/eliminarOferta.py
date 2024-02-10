from .baseCommand import BaseCommand
from ..models.offer import Offer, db
from flask import request, jsonify
from ..errors.errors import TokenInvalid, TokenMissing, InvalidFormat, OfferNotFound
from ..utils.valid_uuid import is_valid_uuid

class DeleteOfferCommand(BaseCommand):
    def __init__(self, offer_id):
        self.offer_id = offer_id

    def execute(self):
        token = request.headers.get("Authorization").split(' ')[1] if request.headers.get('Authorization') else None
        if not token:
            raise TokenMissing()
        if not is_valid_uuid(token):
            raise TokenInvalid


        if not isinstance(self.offer_id, str) or not is_valid_uuid(self.offer_id):
            raise InvalidFormat()

        offer = Offer.query.get(self.offer_id)

        if offer:
            db.session.delete(offer)
            db.session.commit()
            return jsonify({"msg": "la oferta fue eliminada"}), 200
        else:
            raise OfferNotFound()
