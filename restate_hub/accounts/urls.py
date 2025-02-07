from django.urls import path
from accounts import views  # Import the entire views module
app_name="accounts"
urlpatterns = [
    path('signup/', views.new_user_register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),

    #SFA
    path('sfa/email-code/<int:usr_id>/<str:u_code>/verify', views.email_kode_verifiy, name="email-code-verification"),
]
