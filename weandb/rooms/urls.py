from django.urls import path
from .views import RoomView, DetailView

urlpatterns = [
    path('', RoomView.as_view()),
    path('/<int:room_no>', DetailView.as_view()),
]
