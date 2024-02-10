from ..repository.interfaces.IPublicacionRepository import IPublicacionRepository

class LimpiarBaseDeDatos():
    def __init__(self, repository: IPublicacionRepository):
        self.repository = repository

    def execute(self):
        return self.repository.cleanDatabase()
    

    
