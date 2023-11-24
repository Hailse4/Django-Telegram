from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import AccountModel 
from .models import ChatModel


class ChatRoomView(LoginRequiredMixin,ListView):
    model = ChatModel
    template_name = "chat/chatroom.html"
    def get(self,*args,**kwargs):
        return HttpResponse("<h1>404 Not Found</h1>",status=404)
    def get_queryset(self):
        receiver_id = self.request.session.get("receiver_id")
        receiver = AccountModel.objects.get(pk=receiver_id)
        objs1 = ChatModel.objects.filter(sender=self.request.user,receiver=receiver)
        objs2 = ChatModel.objects.filter(sender=receiver,receiver=self.request.user)
        chats = objs1.union(objs2)
        return chats
    

    def post(self,request,*args,**kwargs):
        chatphone = request.POST.get("chatphone")
        sender = request.user
        obj = AccountModel.objects.get(phone="+251"+chatphone)
        request.session['receiver_id'] = obj.id
        chats = self.get_queryset()
        context = {
            'receiver':obj,
            'sender':sender,
            "chats":chats
        }
        return render(request,"chat/chatroom.html",context)
    
    