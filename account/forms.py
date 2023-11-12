from django import forms
from .models import AccountModel
from string import punctuation,digits 

class AccountForm(forms.Form):
    username = forms.CharField(max_length=100,min_length=2)
    password = forms.CharField(max_length=100,label="password")
    cpassword = forms.CharField(max_length=100,label="Confirm Password")
    def clean_username(self):
        username = self.cleaned_data['username']
        exist = AccountModel.objects.filter(username=username).exists()
        if exist:
            self.add_error('username','Already Exist')
        return username
    def clean_password(self):
        password = self.cleaned_data['password']
        contain_symbol = any(char in punctuation for char in password)
        contain_digit = any(char in digits for char in password)
        print(contain_symbol,contain_digit)
        if len(password) < 8:
            self.add_error('password','min length is 8')  
        if not (contain_symbol and contain_digit):
            print("whyyyy")
            self.add_error('password',"password must contain symbol and number")
        return password
    def clean_cpassword(self):
        cpassword = self.cleaned_data['cpassword']
        password = self.cleaned_data['password']
        contain_symbol = any(char in punctuation for char in cpassword)
        contain_digit = any(char in digits for char in cpassword)
        if password != cpassword:
            self.add_error('cpassword','password does not match with above password')
        return cpassword 
        
        
    
    