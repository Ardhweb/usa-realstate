from django.urls import path
from apiroot.core.views import CoreCountry,CoreState,CoreCity,CoreCounty

urlpatterns = [
    path('countries/', CoreCountry.as_view(), name='countries-api'),
    path('states/', CoreState.as_view(), name='state-api'),
    path('counties/', CoreCounty.as_view(), name='county-api'),
    path('cities/', CoreCity.as_view(), name='city-api'),
  

]