import json
import jwt
import bcrypt
import requests

from django.http        import JsonResponse
from django.views       import View
from .models            import Users, SocialPlatform
from weandb.settings    import SECRET_KEY

class SignUpView(View) :
    def post(self, request) :
        credential      = json.loads(request.body)
        hashed_password = bcrypt.hashpw(credential["password"].encode('utf-8'), bcrypt.gensalt())
        Users(
            email       = credential["email"],
            password    = hashed_password.decode("utf-8")
        ).save()

        return JsonResponse({"MESSAGE":"SUCCESS"}, status=200)

        if not Users.objects.filter(email = credential["email"]).exists() :
            hashed_password = bcrypt.hashpw(credential["password"].encode('utf-8'), bcrypt.gensalt())
            Users(
                first_name  = credential["first_name"],
                last_name   = credential["last_name"],
                email       = credential["email"],
                password    = hashed_password.decode("utf-8"),
                birth_year  = credential["birth_year"],
                birth_month = credential["birth_month"],
                birth_day   = credential["birth_day"]
            ).save()
            return JsonResponse({"message":"SUCCESS"}, status=200)
        else :
            return JsonResponse({"message":"EXIST_USER"}, status=400)

class SignInView(View) :
    def post(self, request) :
        credential  = json.loads(request.body)

        try :
            user = Users.objects.get(email=credential["email"])
            if bcrypt.checkpw(credential["password"].encode("utf-8"), user.password.encode("utf-8")) :
                payload             = {"user_id" : user.id}
                encryption_secret   = SECRET_KEY
                algorithm           = "HS256"
                encoded             = jwt.encode(payload, encryption_secret, algorithm=algorithm)
                return JsonResponse({"access_token":encoded.decode("utf-8")}, status=200)
            else :
                return JsonResponse({"message":"INVALID_PASSWORD"}, status=401)
        except Users.DoesNotExist:
            return JsonResponse({"message":"INVALID_EMAIL"}, status=401)

class KakaoSignInView(View) :
   def get(self, request) :
        kakao_access_token  = request.headers["Authorization"]
        headers             = {'Authorization' : f"Bearer {kakao_access_token}"} 
        URL                 = "https://kapi.kakao.com/v2/user/me"
        response            = requests.get(URL, headers = headers)
        kakao_user_info     = response.json()
 
        if Users.objects.filter(social_id = kakao_user_info['id']).exists() :
            user                    = Users.objects.get(social_id=kakao_user_info['id'])
            payload                 = {"user_id" : user.id}
            encryption_secret       = SECRET_KEY
            algorithm               = "HS256"
            encoded_access_token    = jwt.encode(payload, encryption_secret, algorithm=algorithm)
            return JsonResponse({"access_token":encoded_access_token.decode("utf-8")}, status=200)

        else :
            Users(
                social_platform_id  = SocialPlatform.objects.get(platform = "kakao").id,
                social_id           = kakao_user_info['id'],
                first_name          = kakao_user_info['properties']['nickname'],
                email               = kakao_user_info['kakao_account']['email']
            ).save()
            user                    = Users.objects.get(social_id=kakao_user_info['id'])
            payload                 = {"user_id" : user.id}
            encryption_secret       = SECRET_KEY
            algorithm               = "HS256"
            encoded_access_token    = jwt.encode(payload, encryption_secret, algorithm=algorithm)
            return JsonResponse({'access_token': encoded_access_token.decode('utf-8')}, status=200)
