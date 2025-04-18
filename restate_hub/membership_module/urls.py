from django.urls import path 
from . import views 

app_name="membership_module"

urlpatterns = [
    path('profile/',views.member_profile, name="member_profile"),
]
