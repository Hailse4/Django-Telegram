from django.contrib.auth.backends import BaseBackend
from .models import AccountModel 
import bcrypt

class AccountModelAuthBackend(BaseBackend):
    def authenticate(self,request,phone=None,password=None):
        try:
            account = AccountModel.objects.get(phone="+251"+phone)
            en_password = bytes(password,"utf-8")
            if bcrypt.checkpw(en_password,account.password):
                return account
        except AccountModel.DoesNotExist:
            return None
    def get_user(self,user_id):
        try:
            account = AccountModel.objects.get(pk=user_id)
            return account
        except DoesNotExist:
            return None
        