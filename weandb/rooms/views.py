import json
import math

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Sum

from .models          import (
    Rooms,
    Pictures,
    RoomsBeds,
    RoomsAmenities,
    RoomsRules
)
from account.models   import (
    Users,
    HostInfos,
    HostInfosLanguages
)

class RoomView(View) :
    def get(self, request):
        offset =         int(request.GET.get('offset', 0))
        limit =          int(request.GET.get('limit', 20))
        counting_all   = Rooms.objects.all().count()
        selected_rooms = Rooms.objects.prefetch_related('pictures_set').all()[offset:limit]
        result_data =    [{
            "id" :       selected_room.id,
            "title" :    selected_room.title,
            "picture" :  selected_room.pictures_set.all()[0].picture,
            } for selected_room in selected_rooms
        ]
        
        return JsonResponse({"rooms_list" : result_data, "total" : counting_all}, status = 200)

class DetailView(View) :
    def get(self, request, room_no):
        try : 
            selected_room =  Rooms.objects.select_related('host', 'room_type', 'refund_policy').prefetch_related('pictures_set', 'roomsbeds_set').get(id = room_no)
            pics =           selected_room.pictures_set.values_list('picture',flat = True)
            beds =           selected_room.roomsbeds_set.aggregate(Sum("number_of_beds"))
            amenities =      selected_room.amenity.values_list('amenity', flat = True)
            rules =          selected_room.rules.values_list('rule', flat = True)
            host_languages = HostInfosLanguages.objects.select_related('language').filter(hostinfo_id = selected_room.host.id)
            language_list =  [
                host_language.language.language
                for host_language in host_languages
            ]
            
            result_data = {
                "id" :            selected_room.id,
                "pic1" :          pics[0],
                "pic2" :          pics[1],
                "pic3" :          pics[2],
                "pic4" :          pics[3],
                "pic5" :          pics[4],
                "name" :          selected_room.title,
                "hostpic" :       selected_room.host.host_image,
                "hostname" :      selected_room.host.nickname,
                "maxpeople" :     selected_room.person_limit,
                "bed" :           beds['number_of_beds__sum'],
                "bathroom" :      selected_room.bathroom,
                "roomtype" :      selected_room.room_type.room_type,
                "roomtypedesc" :  selected_room.room_type.description,
                "roomstory"    :  selected_room.description,
                "utility_count" : len(amenities),
                "utility_list"  : list(amenities),
                "language_list" : language_list,
                "hostintro" :     selected_room.host.intro,
                "warning_list" :  list(rules),
                "refund_policy" : selected_room.refund_policy.policy,
                "refund_desc" :   selected_room.refund_policy.description,
                "price" :         selected_room.fee,
                "cleaning_fee" :  selected_room.cleaning_fee,
                "center" : {
                    "lat" :       selected_room.lat,
                    "lng" :       selected_room.lng,
                }
            }

            return JsonResponse({"room_information" : result_data}, status = 200)

        except Rooms.DoesNotExist : 
            return JsonResponse({"error" : "ROOM_NOT_FOUND"}, status = 404)
