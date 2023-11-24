from django.db import models

class AccountModel(models.Model):
    phone = models.CharField(max_length=13)
    username = models.CharField(max_length=50)
    password = models.BinaryField()
    last_login = models.DateTimeField(auto_now=True)
    is_authenticated = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['date']
    def __str__(self):
        return self.username 
    