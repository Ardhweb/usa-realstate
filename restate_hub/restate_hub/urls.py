"""
URL configuration for restate_hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings #for MEdia Manging Step4
from django.conf.urls.static import static #For Media Manging and Static step4
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
schema_view = get_schema_view(
    openapi.Info(
        title="Real State Hub API's",
        default_version='v1',
        description="API documentation for your Django REST Framework project.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # You can change the permissions as needed
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('core/', include("core.urls")),
    path('agents/', include("agent_module.urls")),
    path('accounts/', include("accounts.urls")),
    path('members/', include("membership_module.urls")),
    path('property/', include("property_module.urls")),
    path('api-auth/', include('rest_framework.urls')), # intending to use the browsable API 
    path('api-root/', include('apiroot.urls')), #root of restful api 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#For Media Manging Step4

static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "USA Real State Hub "
admin.site.site_title = "Real State Hub Admin"
admin.site.index_title = "Welcome to Real State Hub"

