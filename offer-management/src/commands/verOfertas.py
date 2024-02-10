from .baseCommand import BaseCommand
from ..models.offer import Offer, OfferSchema
from flask import request, jsonify
from ..errors.errors import TokenInvalid, TokenMissing, InvalidFormat
from ..utils.valid_uuid import is_valid_uuid

class ViewOffersCommand(BaseCommand):
    def __init__(self, post_id=None, owner=None):
        self.post_id = post_id
        self.owner = owner

    def execute(self):
        token = request.headers.get("Authorization").split(' ')[1] if request.headers.get('Authorization') else None
        if not token:
            raise TokenMissing()
        
        if not is_valid_uuid(token):
            raise TokenInvalid()

        query = Offer.query

        if self.post_id is not None and not isinstance(self.post_id, str):
            raise InvalidFormat()
        
        if self.owner is not None and not is_valid_uuid(self.owner) and self.owner != 'me':
            raise InvalidFormat()

        if self.post_id:
            query = query.filter_by(postId=self.post_id)

        if self.owner and self.owner != 'me':
            query = query.filter_by(userId=self.owner)

        filtered_offers = query.all()

        offer_schema = OfferSchema(many=True)
        serialized_offers = offer_schema.dump(filtered_offers)

        return jsonify(serialized_offers), 200