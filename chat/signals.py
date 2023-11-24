from django.db.models.signals import post_save
from django.dispatch import receiver
from chat.models import ChatModel,ChatListModel 


@receiver(post_save,sender=ChatModel)
def create_chat_list_model(sender,instance,created,*args,**kwargs):
    if created:
        s_rexist = ChatListModel.objects.filter(
            sender=instance.sender,receiver=instance.receiver
        ).exists()
        r_sexist = ChatListModel.objects.filter(
            sender=instance.receiver,receiver=instance.sender
        ).exists()
        if s_rexist or r_sexist:
            if s_rexist:
                obj = ChatListModel.objects.filter(sender=instance.sender,receiver=instance.receiver)
            else:
                obj = ChatListModel.objects.filter(sender=instance.receiver,receiver=instance.sender)
            obj.update(
                sender=instance.sender,receiver=instance.receiver,
                message=instance.message,time=instance.time
            )
        else:
            ChatListModel.objects.create(
                sender=instance.sender,receiver=instance.receiver,
                message=instance.message,time=instance.time
            )
            
         