from django.urls import path
from .consumers import ChatRoomConsumer,ChatListConsumer


websocket_urlpatterns = [
    path("ws/chatroom/",ChatRoomConsumer.as_asgi()),
    path("ws/chatlist/",ChatListConsumer.as_asgi()),
]