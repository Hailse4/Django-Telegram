from django.contrib.auth.backends import BaseBackend
from .models import AccountModel 

class AccountModelAuthBackend(BaseBackend):
    def authenticate(self,request,phone,password):
        try:
            account = AccountModel.objects.get(phone=phone)
            if 
        except AccountModel.DoesNotExist:
            return None
        