from django.urls import path 
from . import views 

app_name="membership_module"

urlpatterns = [
    path('profile/',views.memebers_profile, name="member_profile"),
]
