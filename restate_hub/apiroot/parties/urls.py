from django.urls import path
from apiroot.parties.views import PropertyList

urlpatterns = [
    path('properties-list/', PropertyList.as_view(), name='properties_list'),

]