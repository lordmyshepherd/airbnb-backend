from django.urls    import path
from .views         import (
                            LanguageView, 
                            RoomTypeView,
                            AmenitiesView,
                            BedTypeView,
                            PolicyView,
                            RuleView,
                            HostImageView, 
                            HostInfoView,
                            RoomInfoView,
                            RoomImagesView,
                            )
urlpatterns = [
    path('', LanguageView.as_view()),
    path('/room_type',RoomTypeView.as_view()),
    path('/amenities',AmenitiesView.as_view()),
    path('/bed_type', BedTypeView.as_view()),
    path('/policy',PolicyView.as_view()),
    path('/rule', RuleView.as_view()),
    path('/host_info', HostInfoView.as_view()),
    path('/host_image', HostImageView.as_view()),
    path('/room_info', RoomInfoView.as_view()),
    path('/room_images', RoomImagesView.as_view())
]
