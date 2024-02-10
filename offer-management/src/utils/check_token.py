from flask import jsonify
from .valid_uuid import is_valid_uuid
from ..errors.errors import TokenInvalid, TokenMissing

def check_token(token):
    if token is None:
        raise TokenMissing()

    if is_valid_uuid(token) is False:
        raise TokenInvalid()

    return None
    