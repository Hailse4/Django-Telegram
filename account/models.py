from django.db import models

class AccountModel(models.Model):
    phone = models.CharField(max_length=13)
    username = models.CharField(max_length=50)
    password = models.BinaryField()
    last_login = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username 
    