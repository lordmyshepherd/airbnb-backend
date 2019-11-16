import json
import jwt
import bcrypt
import unittest

from django.test        import Client, TestCase
from account.models     import Users
from unittest.mock      import patch, MagicMock

class UserSignInTest(unittest.TestCase) :

    def setUp(self) :
        password        = 'hello123'
        byted_password  = bytes(password, 'utf-8')
        hashed_password = bcrypt.hashpw(byted_password, bcrypt.gensalt())

        Users(
            first_name      = 'sunghun',
            last_name       = 'choo',
            email           = 'ufc@gmail.com',
            password        = hashed_password.decode('utf-8'),
            birth_year_id   = 1,
            birth_month_id  = 4,
            birth_day_id    = 10
        ).save()

    def tearDown(self) :
        Users.objects.get(email='ufc@gmail.com').delete()
        try :
            Users.objects.get(social_id=11).delete()
        except :
            pass

    def test_email_sign_in(self):
        c = Client()

        user_info       = {'email' : 'ufc@gmail.com', 'password' : 'hello123'}
        response        = c.post('/account/signin', json.dumps(user_info), content_type='applications/json')
        self.assertEqual(response.status_code, 200)

    @patch('account.views.requests')
    def test_kakao_sign_in(self, mocked_requests) :
        c = Client()

        class FakeResponse:
            def json(self):
                return {
                    "id" : "11",
                    "properties" : {"nickname" : "BAM"},
                    "kakao_account" : {"email" : "gogo@gmail.com"}
                }

        mocked_requests.get = MagicMock(return_value = FakeResponse())
        header = {'HTTP_Authorization' : '1234ABCD'}
        response = c.get('/account/kakao_signin', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
