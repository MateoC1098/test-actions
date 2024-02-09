from abc import ABC, abstractmethod

class IPublicacionRepository(ABC):

    @abstractmethod
    def savePost(self, publicacion):
        pass

    @abstractmethod
    def readPost(self,id):
        pass

    @abstractmethod
    def deletePost(self, id):
        pass

    @abstractmethod
    def readAllPost(self,filters):
        pass

    @abstractmethod
    def cleanDatabase(self):
        pass