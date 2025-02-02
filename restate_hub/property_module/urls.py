from django.urls import path 
from . import views 

app_name = "property_module"
urlpatterns = [
    path('list/', views.property_listing , name="property-listing"),
    path('add/', views.add_property, name="property-add"),
]
