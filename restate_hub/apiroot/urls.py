from django.urls import path, include

urlpatterns = [
    path('parties/', include('apiroot.parties.urls')),  # Include app1 API URLs
    path('core/', include('apiroot.core.urls')),  # Include app1 API URLs
 
]