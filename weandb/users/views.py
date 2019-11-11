import json
import jwt
import bcrypt
from django.http    import JsonResponse
from django.views   import View
from .models        import Users

class SignUpView(View) :
    def post(self, request) :
        data            = json.loads(request.body)
        password        = data["password"]
        hashed_password = bcrypt.hashpw(b"password", bcrypt.gensalt())

        Users(
            email       = data["email"],
            password    = hashed_password.decode("utf-8")
        ).save()

        return JsonResponse({"MESSAGE":"SUCCESS"}, status=200)
