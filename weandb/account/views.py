import json
import jwt
import bcrypt
import requests

from django.http        import JsonResponse
from django.views       import View
from weandb.settings    import SECRET_KEY

from .models            import Users, SocialPlatform, Years, Months, Days

class YearView(View) :
    def get(self, request) :
        return JsonResponse({"year_list" : list(Years.objects.values())}, status = 200)

class MonthView(View) :
    def get(self, request) :
        return JsonResponse({"month_list" : list(Months.objects.values())}, status = 200)

class DayView(View) :
    def get(self, request) :
        return JsonResponse({"day_list" : list(Days.objects.values())}, status = 200)

class SignUpView(View) :
    def post(self, request) :
        credential      = json.loads(request.body)
        hashed_password = bcrypt.hashpw(credential["password"].encode('utf-8'), bcrypt.gensalt())

        if not Users.objects.filter(email = credential["email"]).exists() :
            Users(
                first_name      = credential["first_name"],
                last_name       = credential["last_name"],
                email           = credential["email"],
                password        = hashed_password.decode("utf-8"),
                birth_year_id   = credential["birth_year"][0]["id"],
                birth_month_id  = credential["birth_month"][0]["id"],
                birth_day_id    = credential["birth_day"][0]["id"]
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
