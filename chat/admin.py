from django.contrib import admin
from chat.models import ChatModel,ChatListModel


admin.site.register(ChatModel)
admin.site.register(ChatListModel)