from unittest import TestCase, mock
from faker import Faker
from ...src.main import app
from ...src.models.publicacion import Publicacion
from datetime import timedelta, datetime


class TestEndpoints(TestCase):
    
        def setUp(self):
            self.app = app.test_client()
            self.fake = Faker()
            now_date = datetime.now() + timedelta(days=1)
            self.publicacion = Publicacion(routeId=self.fake.uuid4(), userId=self.fake.uuid4(), expireAt=self.fake.date_between_dates(date_start=now_date, date_end=now_date + timedelta(days=3)))
            self.publicacion.id = self.fake.uuid4()
            self.publicacion.createdAt = self.fake.date_time_this_year(before_now=True, tzinfo=None)
            self.json_data = {
                'routeId': self.publicacion.routeId,
                'expireAt': self.publicacion.expireAt.strftime('%Y-%m-%dT%H:%M:%S')+'.214Z'
            }

            self.headers = {
                'Authorization': f'Bearer {self.publicacion.userId}'
            }
                
    
        @mock.patch('src.commands.crear_publicacion.CrearPublicacion.execute')
        def test_crear_publicacion_exitoso(self,mock_execute):

            mock_execute.return_value = ({
                'id': self.publicacion.id,
                'userId': self.publicacion.userId,
                'createdAt': self.publicacion.createdAt.isoformat()
            },201)

            expected_response = {
                'id': self.publicacion.id,
                'userId': self.publicacion.userId,
                'createdAt': self.publicacion.createdAt.isoformat()
            }

            response = self.app.post('/posts', json=self.json_data, headers=self.headers)

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json, expected_response)

        @mock.patch('src.commands.crear_publicacion.CrearPublicacion.execute')
        def test_create_post_token_invalido(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },400)


            wrong_headers = {
                'Authorization': f'Bearer uuidinvalido'
            }

            response = self.app.post('/posts', json=self.json_data, headers=wrong_headers)

            self.assertEqual(response.status_code, 401)

        @mock.patch('src.commands.crear_publicacion.CrearPublicacion.execute')
        def test_crear_publicacion_sin_token(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },400)

            response = self.app.post('/posts', json=self.json_data)

            self.assertEqual(response.status_code, 403)

        @mock.patch('src.commands.crear_publicacion.CrearPublicacion.execute')
        def test_crear_publicacion_sin_campo_expireAt(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },400)


            response = self.app.post('/posts', json={'routeId': self.publicacion.routeId}, headers=self.headers)

            self.assertEqual(response.status_code, 400)

        @mock.patch('src.commands.crear_publicacion.CrearPublicacion.execute')
        def test_crear_publicacion_sin_campo_routeId(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },400)

            response = self.app.post('/posts', json={'expireAt': self.publicacion.expireAt.strftime('%Y-%m-%dT%H:%M:%S')}, headers=self.headers)

            self.assertEqual(response.status_code, 400)

        @mock.patch('src.commands.crear_publicacion.CrearPublicacion.execute')
        def test_crear_publicacion_con_routeId_invalido(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },400)

            response = self.app.post('/posts', json={'routeId': 'uuidinvalido', 'expireAt': self.publicacion.expireAt.strftime('%Y-%m-%dT%H:%M:%S')}, headers=self.headers)

            self.assertEqual(response.status_code, 400)

        @mock.patch('src.commands.crear_publicacion.CrearPublicacion.execute')
        def test_crear_publicacion_con_fecha_invalida(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },400)

            response = self.app.post('/posts', json={'routeId': self.publicacion.routeId, 'expireAt': 'fecha invalida'}, headers=self.headers)

            self.assertEqual(response.status_code, 400)

        @mock.patch('src.commands.crear_publicacion.CrearPublicacion.execute')
        def test_crear_publicacion_con_fecha_expirada(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },400)

            response = self.app.post('/posts', json={'routeId': self.publicacion.routeId, 'expireAt': self.fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None).strftime('%Y-%m-%dT%H:%M:%S')+'.214Z'}, headers=self.headers)

            self.assertEqual(response.status_code, 412)

        @mock.patch('src.commands.ver_publicaciones.VerPublicaciones.execute')
        def test_ver_publicaciones_exitoso(self,mock_execute):

            mock_execute.return_value = [{
                'id': self.publicacion.id,
                'userId': self.publicacion.userId,
                'createdAt': self.publicacion.createdAt.isoformat()
            }]

            expected_response = [{
                'id': self.publicacion.id,
                'userId': self.publicacion.userId,
                'createdAt': self.publicacion.createdAt.isoformat()
            }]

            response = self.app.get('/posts', headers=self.headers)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, expected_response)

        @mock.patch('src.commands.ver_publicaciones.VerPublicaciones.execute')
        def test_ver_publicaciones_con_parametro_expire_invalido(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },400)

            response = self.app.get('/posts?expire=invalido', headers=self.headers)

            self.assertEqual(response.status_code, 400)

        @mock.patch('src.commands.ver_publicaciones.VerPublicaciones.execute')
        def test_ver_publicaciones_con_parametro_route_invalido(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },400)

            response = self.app.get('/posts?route=invalido', headers=self.headers)

            self.assertEqual(response.status_code, 400)

        @mock.patch('src.commands.ver_publicaciones.VerPublicaciones.execute')
        def test_ver_publicaciones_con_parametro_owner_invalido(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },400)

            response = self.app.get('/posts?owner=invalido', headers=self.headers)

            self.assertEqual(response.status_code, 400)

        @mock.patch('src.commands.ver_publicaciones.VerPublicaciones.execute')
        def test_ver_publicaciones_token_invalido(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },400)

            wrong_headers = {
                'Authorization': f'Bearer uuidinvalido'
            }

            response = self.app.get('/posts', headers=wrong_headers)

            self.assertEqual(response.status_code, 401)

        @mock.patch('src.commands.ver_publicaciones.VerPublicaciones.execute')
        def test_ver_publicaciones_sin_token(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },400)

            response = self.app.get('/posts')

            self.assertEqual(response.status_code, 403)

        @mock.patch('src.commands.consultar_publicacion.ConsultarPublicacion.execute')
        def test_consultar_publicacion_exitoso(self,mock_execute):

            mock_execute.return_value = ({
                'id': self.publicacion.id,
                'routeId': self.publicacion.routeId,
                'userId': self.publicacion.userId,
                'expireAt': self.publicacion.expireAt.isoformat(),
                'createdAt': self.publicacion.createdAt.isoformat()
            })

            expected_response = {
                'id': self.publicacion.id,
                'routeId': self.publicacion.routeId,
                'userId': self.publicacion.userId,
                'expireAt': self.publicacion.expireAt.isoformat(),
                'createdAt': self.publicacion.createdAt.isoformat()
            }

            response = self.app.get(f'/posts/{self.publicacion.id}', headers=self.headers)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, expected_response)

        @mock.patch('src.commands.consultar_publicacion.ConsultarPublicacion.execute')
        def test_consultar_publicacion_con_id_invalido(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },404)

            response = self.app.get('/posts/invalidoid', headers=self.headers)

            self.assertEqual(response.status_code, 400)

        @mock.patch('src.commands.consultar_publicacion.ConsultarPublicacion.execute')
        def test_consultar_publicacion_id_no_existe(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },404)

            response = self.app.get(f'/posts/{self.publicacion.id}', headers=self.headers)

            self.assertEqual(response.status_code, 404)


        @mock.patch('src.commands.consultar_publicacion.ConsultarPublicacion.execute')
        def test_consultar_publicacion_token_invalido(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },401)

            wrong_headers = {
                'Authorization': f'Bearer uuidinvalido'
            }

            response = self.app.get(f'/posts/{self.publicacion.id}', headers=wrong_headers)

            self.assertEqual(response.status_code, 401)

        @mock.patch('src.commands.consultar_publicacion.ConsultarPublicacion.execute')
        def test_consultar_publicacion_sin_token(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },403)

            response = self.app.get(f'/posts/{self.publicacion.id}')

            self.assertEqual(response.status_code, 403)

        @mock.patch('src.commands.eliminar_publicacion.EliminarPublicacion.execute')
        def test_eliminar_publicacion_exitoso(self,mock_execute):

            mock_execute.return_value = ({
                'msg': 'la publicación fue eliminada'
            },200)

            response = self.app.delete(f'/posts/{self.publicacion.id}', headers=self.headers)

            self.assertEqual(response.status_code, 200)

        @mock.patch('src.commands.eliminar_publicacion.EliminarPublicacion.execute')
        def test_eliminar_publicacion_con_id_invalido(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },400)

            response = self.app.delete('/posts/invalidoid', headers=self.headers)

            self.assertEqual(response.status_code, 400)

        @mock.patch('src.commands.eliminar_publicacion.EliminarPublicacion.execute')
        def test_eliminar_publicacion_id_no_existe(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },404)

            response = self.app.delete(f'/posts/{self.publicacion.id}', headers=self.headers)

            self.assertEqual(response.status_code, 404)

        @mock.patch('src.commands.eliminar_publicacion.EliminarPublicacion.execute')
        def test_eliminar_publicacion_token_invalido(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },401)

            wrong_headers = {
                'Authorization': f'Bearer uuidinvalido'
            }

            response = self.app.delete(f'/posts/{self.publicacion.id}', headers=wrong_headers)

            self.assertEqual(response.status_code, 401)

        @mock.patch('src.commands.eliminar_publicacion.EliminarPublicacion.execute')
        def test_eliminar_publicacion_sin_token(self,mock_execute):

            mock_execute.return_value = ({
                'error': 'Error'
            },403)

            response = self.app.delete(f'/posts/{self.publicacion.id}')

            self.assertEqual(response.status_code, 403)

        @mock.patch('src.commands.borrar_datos_db.LimpiarBaseDeDatos.execute')
        def test_limpiar_base_de_datos_exitoso(self,mock_execute):

            mock_execute.return_value = ({
                'msg': 'Todos los datos fueron eliminados'
            },200)

            response = self.app.post('/posts/reset', headers=self.headers)

            self.assertEqual(response.status_code, 200)

        def test_ping_exitoso(self):

            response = self.app.get('/posts/ping')

            self.assertEqual(response.status_code, 200)

        
        
    
