from ..repository.interfaces.IPublicacionRepository import IPublicacionRepository

class VerPublicaciones():
    def __init__(self, repository: IPublicacionRepository):
        self.repository = repository

    def execute(self, filters):
        return self.repository.readAllPost(filters)