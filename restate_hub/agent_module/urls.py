from django.urls import path 
from . import views 

app_name = "agent_module"
urlpatterns = [
    path('agent/<str:agent_id>/', views.agent_detail, name='agent_detail'),
   
]