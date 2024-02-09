from unittest import TestCase, mock
from faker import Faker
from src.models.publicacion import Publicacion
from src.commands.eliminar_publicacion import EliminarPublicacion

class TestEliminarPublicacion(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.repository = mock.Mock()
        self.eliminar_publicacion = EliminarPublicacion(repository=self.repository)

    def test_execute(self):
        publicacion = Publicacion(routeId=self.fake.uuid4(), userId=self.fake.uuid4(), expireAt=self.fake.date_time())
        publicacion.id = self.fake.uuid4()
        publicacion.createdAt = self.fake.date_time()
        self.repository.deletePost.return_value = ({'msg':'la publicación fue eliminada'}, 200)
        response=self.eliminar_publicacion.execute(publicacion.id)
        self.assertEqual(response, ({'msg':'la publicación fue eliminada'}, 200))
