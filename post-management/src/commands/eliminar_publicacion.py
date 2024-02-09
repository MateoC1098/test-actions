from ..repository.interfaces.IPublicacionRepository import IPublicacionRepository

class EliminarPublicacion():
    def __init__(self, repository: IPublicacionRepository):
        self.repository = repository

    def execute(self, id):
        return self.repository.deletePost(id)