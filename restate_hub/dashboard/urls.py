from django.urls import path 
from . import views 

app_name="dashboard"

urlpatterns = [
    path('', views.admin_custom_dashboard, name="dashboard"),
    path('membership-fee/', views.membership_fee, name="membershipfee"),
    path('accounts/',views.accounts_page, name="accounts_page"),
   
]
