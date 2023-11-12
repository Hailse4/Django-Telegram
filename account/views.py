from django.shortcuts import render, redirect 
from django.http import JsonResponse,Http404
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from twilio.rest import Client
from .getverifycode import ExpiringDict
from .models import AccountModel 
from .forms import AccountForm
import random 
import bcrypt
account_sid = "AC7e4ac1f6a8a969a460c2a0cd3e4ff261"

auth_token = "d40234c24960acff714e7b858847a5c1"

setverifycode = ExpiringDict()
get_phone = {}

def VerifyPhone(request):
    print("twist")
    if request.method == "POST":
        type_ = request.POST.get('type')
        if type_ == "getcode":
            phone = request.POST.get('phone')
            client = Client(account_sid,auth_token)
            code = random.randint(100000,900000)
            print("your code",code)
            phone_exist = AccountModel.objects.filter(phone="+251"+phone).exists()
            if len(phone) != 9:
                print("is not happening length")
                return JsonResponse(data={"validate":"is not valid length","valid":False})
            elif not str(phone).startswith("9") and type(phone) != type(1) :
                print("is not happening Format ")
                return JsonResponse(data={"validate":"is not valid format","valid":False})
            elif phone_exist:
                data={'validate':'account with phone number already exist','valid':False}
                return JsonResponse(data=data)
            else:
                setverifycode.set(phone,code,60)
                get_phone["phone"] = phone 
                '''message = client.messages.create(
                    body=f"your telegram verification code is {code}",
                    from_="+14435525169",
                    to="+251"+phone
                )'''
                return JsonResponse(data={"valid":True,"validate":""})
            
            

        elif type_ == "verify":
            try:
                user_code = int(request.POST.get('code'))
            except ValueError:
                data = {'resp':'invalid character','redirect':False}
                return JsonResponse(data=data)
            print("user code",user_code+1)
            
            phone = get_phone["phone"]
            code = setverifycode.get(phone)
            if user_code == code:
                request.session["phone"] = phone
                url = reverse_lazy("create-account")
                data = {"url":url,'redirect':True}
                return JsonResponse(data=data)
                
            else:
                data = {'resp':"code dose not matched",'redirect':False}
                return JsonResponse(data=data)
            
            
        
            
    return render(request,'account/verifyphone.html')


class CreateAccountView(FormView):
    form_class = AccountForm
    template_name = "account/create_account.html"
    def get(self,*args,**kwargs):
        phone = self.request.session.get("phone",False)
        if not phone:
            raise Http404
        return super().get(*args,**kwargs,form=self.get_form())
    def post(self,request,*args,**kwargs):
        phone = request.session.get("phone",False)
        if not phone:
            raise Http404
        data = {
            "username":request.POST.get("username"),
            "password":request.POST.get("password"),
            "cpassword":request.POST.get("cpassword")
        }
        a_form = AccountForm(data=data)
        if a_form.is_valid():
            cleaned_data = a_form.cleaned_data
            del cleaned_data["cpassword"]
            password = bytes(cleaned_data["password"],"utf-8")
            cleaned_data["password"] = bcrypt.hashpw(password,bcrypt.gensalt())
            cleaned_data["phone"] = "+251" + phone 
            AccountModel.objects.create(**cleaned_data)
            del request.session["phone"]
            print("account created successfully")
        else:
            print("form is invalid")
            return self.form_invalid(a_form)
            
            
            
        