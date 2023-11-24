from django.db import models
from account.models import AccountModel 

class ChatModel(models.Model):
    sender = models.ForeignKey(AccountModel,on_delete=models.CASCADE)
    receiver = models.ForeignKey(AccountModel,on_delete=models.CASCADE,related_name="message_reveiver")
    message = models.TextField()
    time = models.TimeField(auto_now_add=True)
    def __str__(self):
        str_ = self.sender.username + "_to_" + self.receiver.username
        return str_
    
    
class ChatListModel(models.Model):
    sender = models.ForeignKey(AccountModel,on_delete=models.CASCADE,related_name="sender_account")
    receiver = models.ForeignKey(AccountModel,on_delete=models.CASCADE)
    message = models.TextField()
    time = models.TimeField()
    def __str__(self):
        str_ = self.sender + "_to_" + self.receiver + "chatlist"
        
