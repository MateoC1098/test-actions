from unittest import TestCase, mock
from faker import Faker
from ...src.models.publicacion import Publicacion
from ...src.commands.consultar_publicacion import ConsultarPublicacion

class TestConsultarPublicacion(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.repository = mock.Mock()
        self.consultar_publicacion = ConsultarPublicacion(repository=self.repository)

    def test_execute(self):
        publicacion = Publicacion(routeId=self.fake.uuid4(), userId=self.fake.uuid4(), expireAt=self.fake.date_time())
        publicacion.id = self.fake.uuid4()
        publicacion.createdAt = self.fake.date_time()
        self.repository.readPost.return_value = ({'id': publicacion.id, 'userId': publicacion.userId, 'createdAt': publicacion.createdAt.isoformat()}, 200)
        response=self.consultar_publicacion.execute(publicacion.id)
        self.assertEqual(response, ({'id': publicacion.id, 'userId': publicacion.userId, 'createdAt': publicacion.createdAt.isoformat()}, 200))