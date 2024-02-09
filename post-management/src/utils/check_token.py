from flask import jsonify
from .valid_uuid import is_valid_uuid4

def check_token(token):
    if token is None:
        return jsonify({'msg':'No hay un token valido en la solicitud'}), 403

    if is_valid_uuid4(token) is False:
        return jsonify({'msg':'token invalido'}), 401