from unittest import TestCase, mock
from faker import Faker
from src.models.publicacion import Publicacion
from src.commands.ver_publicaciones import VerPublicaciones

class TestVerPublicaciones(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.repository = mock.Mock()
        self.ver_publicaciones = VerPublicaciones(repository=self.repository)

    def test_execute(self):
        publicacion = Publicacion(routeId=self.fake.uuid4(), userId=self.fake.uuid4(), expireAt=self.fake.date_time())
        publicacion.id = self.fake.uuid4()
        publicacion.createdAt = self.fake.date_time()
        self.repository.readAllPost.return_value = ([{'id': publicacion.id, 'userId': publicacion.userId, 'createdAt': publicacion.createdAt.isoformat()}], 200)
        response=self.ver_publicaciones.execute({})
        self.assertEqual(response, ([{'id': publicacion.id, 'userId': publicacion.userId, 'createdAt': publicacion.createdAt.isoformat()}], 200))