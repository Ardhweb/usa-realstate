from django.urls import path
from accounts import views  # Import the entire views module

urlpatterns = [
    path('signup/', views.new_user_register, name="register"),
]
