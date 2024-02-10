from .base_command import BaseCommannd
from flask import jsonify

class PingCommand(BaseCommannd):
    def __init__(self):
        pass

    def execute(self):
        return jsonify({"pong": "true"}), 200
