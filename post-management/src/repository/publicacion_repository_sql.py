from .interfaces.IPublicacionRepository import IPublicacionRepository
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify

from ..models.publicacion import db,Publicacion,PublicacionSchema


publicacion_schema = PublicacionSchema()

class PublicacionRepositorySQL(IPublicacionRepository):

    def savePost(self, publicacion):

        try:
            db.session.add(publicacion)
            db.session.commit()
            return jsonify({
                'id': publicacion.id,
                'userId': publicacion.userId,
                'createdAt': publicacion.createdAt.isoformat()
            }), 201
        except SQLAlchemyError as e:
            db.session.rollback()

            cod_error = e.orig.pgcode
            if(cod_error is not None):
                error_db = {
                    '22007': 'Error de formato de fecha',
                    '22008': 'Error de formato de fecha',
                    '23505': 'El id de la publicacion ya existe'
                }
                return jsonify({'error': error_db[cod_error]}), 400
            
            return jsonify({'error': error_db[cod_error]}), 500


    def readPost(self, id):
        pass

    def deletePost(self, id):
        pass

    def readAllPost(self,filters):
        if filters == {}:
            post=db.session.query(Publicacion).all()
            return publicacion_schema.dump(post,many=True), 200
        
    def cleanDatabase(self):
        pass
    
