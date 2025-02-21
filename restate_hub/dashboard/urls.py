from django.urls import path 
from . import views 
from . import utils
app_name="dashboard"

urlpatterns = [
    path('', views.admin_custom_dashboard, name="dashboard"),
    path('membership-fee/', views.membership_fee, name="membershipfee"),
    path('accounts/',views.accounts_page, name="accounts_page"),
    path('user_data/',  utils.user_data, name='user_data'),
]
