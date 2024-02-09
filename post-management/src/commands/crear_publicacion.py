from ..repository.interfaces.IPublicacionRepository import IPublicacionRepository

class CrearPublicacion():
    def __init__(self, repository: IPublicacionRepository):
        self.repository = repository

    def execute(self, publicacion):
        return self.repository.savePost(publicacion)