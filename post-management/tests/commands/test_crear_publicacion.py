from unittest import TestCase, mock
from faker import Faker
from src.models.publicacion import Publicacion
from src.commands.crear_publicacion import CrearPublicacion

class TestCrearPublicacion(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.repository = mock.Mock()
        self.crear_publicacion = CrearPublicacion(repository=self.repository)

    def test_execute(self):
        publicacion = Publicacion(routeId=self.fake.uuid4(), userId=self.fake.uuid4(), expireAt=self.fake.date_time())
        publicacion.id = self.fake.uuid4()
        publicacion.createdAt = self.fake.date_time()
        self.repository.savePost.return_value = ({'id': publicacion.id, 'userId': publicacion.userId, 'createdAt': publicacion.createdAt.isoformat()}, 201)
        response=self.crear_publicacion.execute(publicacion)
        self.assertEqual(response, ({'id': publicacion.id, 'userId': publicacion.userId, 'createdAt': publicacion.createdAt.isoformat()}, 201))