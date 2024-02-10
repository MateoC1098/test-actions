from flask import Blueprint, request, jsonify, Flask
from ..commands.crearOferta import CreateOfferCommand
from ..commands.verOferta import ViewOfferCommand
from ..commands.verOfertas import ViewOffersCommand
from ..commands.eliminarOferta import DeleteOfferCommand
from ..commands.resetDatabase import ResetDatabaseCommand
from ..models.offer import Offer, OfferSchema
from ..errors.errors import TokenInvalid, TokenMissing, FieldsMissing, InvalidFormat, InvalidValues, OfferNotFound
import uuid

views = Blueprint('views', __name__)

def handle_error(error):
    response = jsonify({"error": error.description})
    response.status_code = error.code
    return response

@views.route('/offers', methods=['POST'])
def create_offer():
    try:
        data = request.get_json()
        command = CreateOfferCommand(data)
        return command.execute()
    
    except TokenMissing as e:
        return handle_error(e)
    
    except TokenInvalid as e:
        return handle_error(e)

    except FieldsMissing as e:
        return handle_error(e)

    except InvalidFormat as e:
        return handle_error(e)

    except InvalidValues as e:
        return handle_error(e)


@views.route('/offers/<offer_id>', methods=['GET'])
def get_offer(offer_id):
    try:
        command = ViewOfferCommand(offer_id)
        return command.execute()

    except TokenMissing as e:
        return handle_error(e)

    except TokenInvalid as e:
        return handle_error(e)
    
    except InvalidFormat as e:
        return handle_error(e)

    except OfferNotFound as e:
        return handle_error(e)

@views.route('/offers', methods=['GET'])
def get_offers():
    try:
        post_id = request.args.get('post')
        owner = request.args.get('owner')
        command = ViewOffersCommand(post_id=post_id, owner=owner)
        return command.execute()

    except TokenMissing as e:
        return handle_error(e)

    except TokenInvalid as e:
        return handle_error(e)

    except InvalidFormat as e:
        return handle_error(e)
    
@views.route('/offers/<offer_id>', methods=['DELETE'])
def delete_offer(offer_id):
    try:
        command = DeleteOfferCommand(offer_id)
        return command.execute()

    except TokenMissing as e:
        return handle_error(e)

    except TokenInvalid as e:
        return handle_error(e)

    except InvalidFormat as e:
        return handle_error(e)
    
    except OfferNotFound as e:
        return handle_error(e)
    
@views.route('/offers/ping', methods=['GET'])
def ping():
    try:
        return "pong", 200
    except Exception as e:
        return handle_error(e)
    
@views.route('/offers/reset', methods=['POST'])
def reset_database():
    try:
        command = ResetDatabaseCommand()
        return command.execute(), 200
    except Exception as e:
        return handle_error(e)
