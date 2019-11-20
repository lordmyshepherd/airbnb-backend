from django.urls    import path
from .views         import LanguageDropDownView, HostImageView, HostInfoView

urlpatterns = [
    path('', LanguageDropDownView.as_view()),
    path('/host_info', HostInfoView.as_view()),
    path('/host_image', HostImageView.as_view())
]
