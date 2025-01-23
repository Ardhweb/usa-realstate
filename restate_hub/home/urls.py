from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.login_page, name='login'),
    path('member/', views.member_page, name='member'),
    path('property/', views.property_page, name='property')

]