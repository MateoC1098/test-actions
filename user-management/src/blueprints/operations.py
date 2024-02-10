from flask import Flask, jsonify, request, Blueprint
from ..commands.create_user import CreateUserCommand
from ..commands.update_user import UpdateUserCommand
from ..commands.reset_database import ResetDatabaseCommand
from ..commands.create_token import CreateTokenCommand
from ..commands.users_me import UsersMeCommand
from ..commands.ping import PingCommand

import os

operations_blueprint = Blueprint('operations', __name__)

@operations_blueprint.route('/users/ping', methods = ['GET'])
def ping():
    command = PingCommand()
    return command.execute()

@operations_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    command = CreateUserCommand(data)
    return command.execute()


@operations_blueprint.route('/users/<uuid:id>', methods=['PATCH'])
def update_user(id):
    data = request.get_json()
    command = UpdateUserCommand(id, data)
    return command.execute()


@operations_blueprint.route('/users/reset', methods=['POST'])
def reset_database():
    command = ResetDatabaseCommand()
    return command.execute()

@operations_blueprint.route('/users/auth', methods=['POST'])
def create_token():
    data = request.get_json()
    command = CreateTokenCommand(data)
    return command.execute()

@operations_blueprint.route('/users/me', methods=['GET'])
def users_me():
    command = UsersMeCommand()
    return command.execute()
