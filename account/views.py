from django.shortcuts import render
from django.http import JsonResponse 
from twilio.rest import Client
from .getverifycode import ExpiringDict
import random 

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
            
            if len(phone) != 9:
                print("is not happening length")
                return JsonResponse(data={"validate":"is not valid length","valid":False})
            elif not str(phone).startswith("9") and type(phone) != type(1) :
                print("is not happening Format ")
                return JsonResponse(data={"validate":"is not valid format","valid":False})
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
            user_code = int(request.POST.get('code'))
            print("user code",user_code+1)
            print(get_phone["phone"])
            code = setverifycode.get(get_phone["phone"])
            if user_code == code:
                data = {'resp':"code matched"}
                return JsonResponse(data=data)
            else:
                data = {'resp':"code dose not matched"}
                return JsonResponse(data=data)
            
            
        
            
    return render(request,'account/verifyphone.html')
