from .interfaces.IPublicacionRepository import IPublicacionRepository
from flask import jsonify
import uuid
from datetime import datetime
from ..models.publicacion import PublicacionSchema

publicacion_schema = PublicacionSchema()



class PublicacionRepositoryMock(IPublicacionRepository):
    def __init__(self):
        self.publicaciones = []

    def savePost(self, publicacion):
        publicacion.id = str(uuid.uuid4())
        publicacion.createdAt = datetime.now()
        self.publicaciones.append(publicacion)
        return jsonify({
                'id': publicacion.id,
                'userId': publicacion.userId,
                'createdAt': publicacion.createdAt.isoformat()
            }), 201
    
    def readPost(self, id):
        publicacion = next((post for post in self.publicaciones if post.id == id), None)
        if publicacion is None:
            return jsonify({'msg':'Publicacion no encontrada'}), 404
        return publicacion_schema.dump(publicacion), 200

    def deletePost(self, id):
        publicacion = next((post for post in self.publicaciones if post.id == id), None)
        if publicacion is None:
            return jsonify({'msg':'Publicacion no encontrada'}), 404
        self.publicaciones.remove(publicacion)
        return jsonify({'msg':'la publicación fue eliminada'}), 200

    def readAllPost(self,filters):
        if filters == {}:
            return publicacion_schema.dump(self.publicaciones,many=True), 200
        
        filtered_posts = self.publicaciones
        
        if 'expire' in filters:
            if filters['expire'] == 'true':
                filtered_posts = [post for post in filtered_posts if post.expireAt <= datetime.now()]
            elif filters['expire'] == 'false':
                filtered_posts = [post for post in filtered_posts if post.expireAt  > datetime.now()]
        
        if 'route' in filters:
            filtered_posts = [post for post in filtered_posts if post.routeId == filters['route']]

        if 'owner' in filters:
            filtered_posts = [post for post in filtered_posts if post.userId == filters['owner']]

        return publicacion_schema.dump(filtered_posts,many=True), 200
    
    def cleanDatabase(self):
        self.publicaciones = []
        return jsonify({'msg':'Todos los datos fueron eliminados'}), 200
        
