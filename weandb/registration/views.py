import json
import boto3

from django.http        import JsonResponse, HttpResponse
from django.views       import View
from django.db          import transaction

from weandb.settings    import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

from account.utils      import login_required
from account.models     import Users, Languages, HostInfos, HostInfosLanguages

from rooms.models       import RoomTypes, Amenities, Beds, RefundPolicies, Rules, Rooms, RoomsAmenities, RoomsRules, RoomsBeds, Pictures

class LanguageView(View) :
    def get(self, request) : 
        return JsonResponse({'languages' : list(Languages.objects.values())}, status = 200)

class RoomTypeView(View) :
    def get(self, request) :
        return JsonResponse({'room_types' : list(RoomTypes.objects.values())}, status = 200)

class AmenitiesView(View) : 
    def get(self, request) :
        return JsonResponse({'amenities' : list(Amenities.objects.values())}, status = 200)

class BedTypeView(View) : 
    def get(self, request) :
        return JsonResponse({'bed_types' : list(Beds.objects.values())}, status = 200)

class PolicyView(View) : 
    def get(self, request) :
        return JsonResponse({'refund_policies' : list(RefundPolicies.objects.values())}, status = 200)

class RuleView(View) : 
    def get(self, request) :
        return JsonResponse({'rules' : list(Rules.objects.values())}, status = 200)
 
class HostInfoView(View) :
    @login_required
    @transaction.atomic
    def post(self, request) :
        data = json.loads(request.body)
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

class RoomInfoView(View) :
    @login_required
    @transaction.atomic
    def post(self, request) :
        data = json.loads(request.body)
        try :
            host = HostInfos.objects.get(user_id = request.user.id)
            room = Rooms(
                host_id             = host.id,
                room_type_id        = int(data["room_type_id"][0]["id"]),
                refund_policy_id    = int(data["refund_policy_id"][0]["id"]),
                title               = data["title"],
                description         = data["description"],
                person_limit        = data["person_limit"],
                bathroom            = data["bathroom"],
                cleaning_fee        = data["cleaning_fee"],
                fee                 = data["fee"],
                lat                 = data["lat"],
                lng                 = data["lng"]
            )
            room.save()

            rooms_amenities_list = [
                RoomsAmenities(
                    room_id     = room.id,
                    amenity_id  = int(amenity["id"])
                ) for amenity in data["amenitiy_list"]
            ]
            
            rooms_beds_list = [
                RoomsBeds(
                    room_id        = room.id,
                    bed_id         = int(bed["id"]),
                    number_of_beds = data["number_of_beds"]
               ) for bed in data["bed_type_list"]
            ]
            
            rooms_rules_list = [
                RoomsRules(
                    room_id = room.id,
                    rule_id = int(rule["id"])
                ) for rule in data["rule_list"]
            ]

            RoomsAmenities.objects.bulk_create(rooms_amenities_list)
            RoomsBeds.objects.bulk_create(rooms_beds_list)
            RoomsRules.objects.bulk_create(rooms_rules_list)
            return JsonResponse({"room_id" : room.id },status = 200)
        except HostInfos.DoesNotExist :
            return JsonResponse({"MESSAGE" : "IVALED_HOST"}, status = 200)

class RoomImagesView(HostImageView) :
    @login_required
    @transaction.atomic
    def post(self, request) :
        try :
            file = request.FILES["room_images"]

            for image in request.FILES.getlist("room_images"):
                Pictures(
                    room_id = int(request.GET.get('room_id')),
                    picture = self.s3_upload(image)
                ).save()
            return HttpResponse(status = 200)
        except Rooms.DoesNotExist :
            return JsonResponse({"MESSAGE":"INVALID_FILE"}, status = 400)
