from django.urls import path
from . import views


urlpatterns = [
    path("chatroom/",views.ChatRoomView.as_view(),name="chatroom"),
]