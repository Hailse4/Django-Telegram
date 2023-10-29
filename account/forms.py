from django import forms


class AccountForm(forms.Form):
    phone = forms.CharField(max_length=13,min_length=13)
    username = forms.CharField(max_length=100,min_length=2)
    password = forms.CharField(max_length=10C,label="password",min_length=8)
    cpassword = forms.CharField(max_length=100,label="Confirm Password",min_length=8)
    
    