import json
import jwt
import bcrypt
import unittest

from weandb.settings                import SECRET_KEY
from django.test                    import Client, TestCase
from unittest.mock                  import patch, MagicMock

from PIL                            import Image
from django.utils.six               import BytesIO
from django.core.files.base         import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

from django.http                    import JsonResponse
from account.utils                  import login_required
from account.models                 import Users, Languages, HostInfos, HostInfosLanguages
from rooms.models                   import RoomTypes, Amenities, Beds, RefundPolicies, Rules, Rooms

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
            first_name      = 'sunghun',
            last_name       = 'choo',
            email           = 'ufc@gmail.com',
            password        = hashed_password.decode('utf-8'),
            birth_year_id   = 12,
            birth_month_id  = 4,
            birth_day_id    = 10
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

    def test_room_registration(self):
        client = Client()
        
        login_info  = {'email' : 'ufc@gmail.com', 'password' : 'hello123'}
        login_response    = client.post('/account/signin', json.dumps(login_info), content_type='applications/json')

        access_token = login_response.json()["access_token"]
        payload = jwt.decode(access_token, SECRET_KEY, 'HS256')
        user_id = payload['user_id']

        HostInfos(
                nickname    = "junjun",
                intro       = "hellow",
                interaction = "kakakakak",
                country     = "korea",
                city        = "seoul",
                user_id     = user_id
        ).save()

        room_info_data = {
                "room_type_id" : [{'id':'1'}],
                "refund_policy_id" : [{'id':'2'}],
                "title" : 'hellow',
                "person_limit" : 3,
                "bathroom" : 2,
                "cleaning_fee" : 1350,
                "fee" : 13500,
                "lat" : 184.30294,
                "lng" : 198.00290,
                "number_of_beds": 3,
                "description" : 'woojung sawoona',
                "amenitiy_list" : [{'id':'1'}, {'id':'3'}],
                "bed_type_list" : [{'id':'1'}, {'id':'4'}],
                "rule_list" : [{'id':'2'}, {'id':'1'}]
        }

        response = client.post(
            '/registration/room_info',
            json.dumps(room_info_data),
            **{'HTTP_Authorization' : access_token },
            content_type='applications/json'
        )
        self.assertEqual(response.status_code, 200)
            
    @patch("registration.views.HostImageView.s3_client")
    def test_room_image_registration(self, mocked_client) :
        client      = Client()

        login_info      = {'email' : 'ufc@gmail.com', 'password' : 'hello123'}
        login_response  = client.post('/account/signin', json.dumps(login_info), content_type='applications/json')
        access_token    = login_response.json()["access_token"]
        payload         = jwt.decode(access_token, SECRET_KEY, 'HS256')
        user_id         = payload['user_id']
        
        host = HostInfos(
            nickname    = "master",
            intro       = "intro",
            interaction = "with frieds",
            country     = "korea",
            city        = "soeul",
            user_id     = user_id
        )
        host.save()

        room = Rooms(
            host_id             = host.id,
            room_type_id        = 1,
            refund_policy_id    = 2,
            title               = "woojung sawoona",
            description         = "inexpensive rooms",
            person_limit        = 5,
            bathroom            = 14,
            cleaning_fee        = 2300,
            fee                 = 149000,
            lat                 = 180.322435,
            lng                 = 29.123425
        )
        room.save()

        stream = BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(stream, format='jpeg')
       
        a_image_file    = SimpleUploadedFile("junhan.jpg", stream.getvalue(), content_type = "image/jpg")
        b_image_file    = SimpleUploadedFile("yeri.jpg", stream.getvalue(), content_type = "image/jpg")
        c_image_file    = SimpleUploadedFile("jihun.jpg", stream.getvalue(), content_type = "image/jpg")

        image_file = [a_image_file, b_image_file, c_image_file]

        response = client.post(
            f"/registration/room_images?room_id={room.id}", 
            {'room_images' : image_file},
            format = 'multipart',
            **{'HTTP_Authorization' : access_token },
        )
        self.assertEqual(response.status_code, 200)
        host.delete()
        room.delete()
