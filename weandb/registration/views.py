import json
import boto3

from django.http        import JsonResponse, HttpResponse
from django.views       import View
from weandb.settings    import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

from account.utils      import login_required
from account.models     import Users, Languages, HostInfos, HostInfosLanguages

class LanguageDropDownView(View) :
    def get(self, request) : 
        language_list = list(Languages.objects.values())
        return JsonResponse({'language_list' : language_list}, status = 200)

class HostInfoView(View) :

    @login_required    
    def post(self, request) :
        data    = json.loads(request.body)
        user_info = Users.objects.filter(id = request.user.id)
        user_info.update(is_host = True)

        host_info = HostInfos.objects.filter(user_id = request.user.id)
        if host_info.exists() :
            host_info.update(
                nickname    = data["nickname"],
                intro       = data["intro"],
                interaction = data["interaction"],
                country     = data["country"],
                city        = data["city"]
            )
        else :
           HostInfos(
                nickname    = data["nickname"],
                intro       = data["intro"],
                interaction = data["interaction"],
                country     = data["country"],
                city        = data["city"],
                user_id     = request.user.id
            ).save()

        language_list = [
                HostInfosLanguages(
                    hostinfo_id    = host_info[0].id,
                    language_id    = language["id"]
                ) for language in data["language_list"]
        ]
        HostInfosLanguages.objects.bulk_create(language_list)

        return HttpResponse(status =200)

class HostImageView(View) :
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )

    def s3_upload(self, file) : 
        self.s3_client.upload_fileobj(
            file,
            "weandb",
            file.name,
            ExtraArgs = {
                "ContentType": file.content_type
            }
        )

        host_image_url = "https://s3.ap-northeast-2.amazonaws.com/weandb/"+file.name
        return host_image_url

    @login_required
    def post(self, request):
        file = request.FILES["host_image"]

        try :
            host_info   = HostInfos.objects.get(user_id = request.user.id)
            image       = self.s3_upload(file)
            HostInfos.objects.filter(user_id = request.user.id).update(host_image = image)
            return HttpResponse(status = 200)

        except HostInfos.DoesNotExist :
            image = self.s3_upload(file)
            HostInfos(
                user_id     = request.user.id,
                host_image  = image
            ).save()
            return HttpResponse(status = 200)
