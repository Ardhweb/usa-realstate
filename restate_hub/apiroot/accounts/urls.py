from django.urls import path
from apiroot.accounts.views import AccountsUser, AgentsAPI

urlpatterns = [
    path('users/', AccountsUser.as_view(), name='account-user-api'),
    path('agents/', AgentsAPI.as_view(), name='account-agent-api'),
   

]