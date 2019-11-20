import json
import jwt
import bcrypt
import unittest

from django.test                    import Client, TestCase
from unittest.mock                  import patch, MagicMock

from PIL                            import Image
from django.utils.six               import BytesIO
from django.core.files.base         import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

from django.http                    import JsonResponse
from account.utils                  import login_required
from account.models                 import Users, Languages, HostInfos, HostInfosLanguages

class GetLanguageListTest(unittest.TestCase) :

    def test_language_drop_down(self) :
        client      = Client()
        response    = client.get('/registration', content_type='applications/json')
        self.assertEqual(response.status_code, 200)

class HostRegistrationTest(unittest.TestCase) :
    
    def setUp(self) :
        password        = 'hello123'
        byted_password  = bytes(password, 'utf-8')
        hashed_password = bcrypt.hashpw(byted_password, bcrypt.gensalt())

        Users(
            first_name  = 'sunghun',
            last_name   = 'choo',
            email       = 'ufc@gmail.com',
            password    = hashed_password.decode('utf-8'),
            birth_year  = 1811,
            birth_month = 4,
            birth_day   = 10
        ).save()

    def tearDown(self) :
        Users.objects.get(email='ufc@gmail.com').delete()
        try :
            Users.objects.get(social_id=11).delete()
        except :
            pass

    @patch("registration.views.HostImageView.s3_client")
    def test_s3_file_upload_test(self, mocked_client) :
        client      = Client()

        login_info  = {'email' : 'ufc@gmail.com', 'password' : 'hello123'}
        response    = client.post('/account/signin', json.dumps(login_info), content_type='applications/json')
        access_token = response.json()["access_token"]
       
        stream = BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(stream, format='jpeg')
        image_file  = SimpleUploadedFile("junhan.jpg", stream.getvalue(), content_type="image/jpg")

        response = client.post(
            '/registration/host_image',
            {'host_image' : image_file},
            format = 'multipart',
            **{'HTTP_Authorization' : access_token }
        )

        self.assertEqual(response.status_code, 200)
