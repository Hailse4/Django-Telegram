from django.db import models

class AccountModel(models.Model):
    phone = models.CharField(max_length=13)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.username 
    