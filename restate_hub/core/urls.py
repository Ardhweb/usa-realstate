from django.urls import path
from core.utils import get_state,get_city_bystate

urlpatterns = [
    path('get-state/', get_state, name="get_state"),
    path('get-city-bystate/<int:state_id>/',get_city_bystate, name="get_city_bystate"),
]
