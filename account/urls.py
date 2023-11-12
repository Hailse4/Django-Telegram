from django.urls import path
from . import views

urlpatterns = [
    path('verify/',views.VerifyPhone,name='verify'),
    path("create/",views.CreateAccountView.as_view(),name="create-account"),
    path("login/",views.account_login_view,name="login"),
    path('logout/',views.account_logout_view,name="logout"),
]

