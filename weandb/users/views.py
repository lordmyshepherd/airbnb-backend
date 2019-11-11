import json
import jwt
import bcrypt
from django.http        import JsonResponse
from django.views       import View
from .models            import Users
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
        except :
            return JsonResponse({"message":"INVALID_EMAIL"}, status=400)
