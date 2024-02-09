from flask import Blueprint, request, jsonify
from ..commands import CrearPublicacion, VerPublicaciones, ConsultarPublicacion, EliminarPublicacion, LimpiarBaseDeDatos
from ..repository.publicacion_repository_mock import PublicacionRepositoryMock
from ..repository.publicacion_repository_sql import PublicacionRepositorySQL
from ..models.publicacion import Publicacion
from ..utils import valid_uuid, iso_format
from datetime import datetime
from ..utils.check_token import check_token
from ..config import AUTHORIZED_PARAMS_FILTER_POST, REQUIERED_BODY_POST


views = Blueprint('views', __name__)


repository = PublicacionRepositoryMock()




@views.route('/posts', methods=['POST'])
def create_post():
    json_data = request.get_json()
    authorization_header = request.headers.get('Authorization').split(' ')[1] if request.headers.get('Authorization') else None

    check_token_result = check_token(authorization_header)
    if check_token_result is not None:
        return check_token_result

    missing_fields = [field for field in REQUIERED_BODY_POST if field not in json_data]
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
    
    routeId = json_data['routeId']
    expireAt = json_data['expireAt']


    if valid_uuid.is_valid_uuid4(routeId) is False or iso_format.is_iso_datetime(expireAt) is False:
        return jsonify({'msg':'Datos en un formato invalido'}), 400
    
    expireAt = datetime.strptime(expireAt, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    if expireAt <= datetime.now():
        return jsonify({'msg':'La fecha expiración no es válida'}), 412
    
    publicacion = Publicacion(routeId=routeId, userId=authorization_header, expireAt=expireAt)

    result = CrearPublicacion(repository=repository).execute(publicacion)
    return result

@views.route('/posts', methods=['GET'])
def get_posts():

    authorization_header = request.headers.get('Authorization').split(' ')[1] if request.headers.get('Authorization') else None
    all_params = request.args.to_dict()

    check_token_result = check_token(authorization_header)
    if check_token_result is not None:
        return check_token_result
    
    filtered_dict = {key: value for key, value in all_params.items() if key in AUTHORIZED_PARAMS_FILTER_POST and value is not None}

    if 'expire' in filtered_dict:
        if filtered_dict['expire'] not in ['true', 'false']:
            return jsonify({'msg':'Parametro expire en un formato invalido'}), 400
        
    if 'route' in filtered_dict:
        if valid_uuid.is_valid_uuid4(filtered_dict['route']) is False:
            return jsonify({'msg':'Parametro route en un formato invalido'}), 400
        
    if 'owner' in filtered_dict:
        if filtered_dict['owner'].lower() == 'me':
            filtered_dict['owner'] = authorization_header

        if valid_uuid.is_valid_uuid4(filtered_dict['owner'])is False:
            return jsonify({'msg':'Parametro owner en un formato invalido'}), 400
        

    if valid_uuid.is_valid_uuid4(authorization_header) is False:
        return jsonify({'msg':'Datos en un formato invalido'}), 400

    result = VerPublicaciones(repository=repository).execute(filtered_dict)
    return result

@views.route('/posts/<id>', methods=['GET'])
def get_post(id):
    authorization_header = request.headers.get('Authorization').split(' ')[1] if request.headers.get('Authorization') else None

    check_token_result = check_token(authorization_header)
    if check_token_result is not None:
        return check_token_result
    
    if valid_uuid.is_valid_uuid4(id) is False:
        return jsonify({'msg':'id en un formato invalido'}), 400
    
    result = ConsultarPublicacion(repository=repository).execute(id)
    return result

@views.route('/posts/<id>', methods=['DELETE'])
def delete_post(id):
    authorization_header = request.headers.get('Authorization').split(' ')[1] if request.headers.get('Authorization') else None

    check_token_result = check_token(authorization_header)
    if check_token_result is not None:
        return check_token_result
    
    if valid_uuid.is_valid_uuid4(id) is False:
        return jsonify({'msg':'id en un formato invalido'}), 400
    
    result = EliminarPublicacion(repository=repository).execute(id)
    return result
    
@views.route('/posts/reset', methods=['POST'])
def reset_posts():    
    result = LimpiarBaseDeDatos(repository=repository).execute()
    return result

@views.route('/posts/ping', methods=['GET'])
def ping():
    return jsonify({'msg':'pong'}), 200