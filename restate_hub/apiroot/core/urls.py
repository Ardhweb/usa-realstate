from django.urls import path
from apiroot.core.views import CoreCountry,CoreState,CoreCity

urlpatterns = [
    path('countries/', CoreCountry.as_view(), name='countries-api'),
    path('states/', CoreState.as_view(), name='state-api'),
    path('cities/', CoreCity.as_view(), name='city-api'),

]