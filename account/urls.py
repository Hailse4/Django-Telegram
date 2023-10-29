from django.urls import path
from . import views

urlpatterns = [
    path('verify/',views.VerifyPhone,name='verify'),
]

