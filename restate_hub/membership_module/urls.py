from django.urls import path 
from . import views 

app_name="membership_module"

urlpatterns = [
    path('profile/',views.member_profile, name="member_profile"),
    path('profile-success/', views.profile_success, name='profile_success'),
    path('dashboard/', views.member_dashboard, name="dashboard"),
    path('dashboard/my-property', views.my_property, name="my_property"),
    path('dashboard/add-property', views.add_property, name="member_add_property"),
    path('dashboard/view-message', views.view_message, name="member_message"),
]
