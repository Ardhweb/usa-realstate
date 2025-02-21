from django.urls import path
from apiroot.accounts.views import AccountsUser

urlpatterns = [
    path('users/', AccountsUser.as_view(), name='account-user-api'),
   

]