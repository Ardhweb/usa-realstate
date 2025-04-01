from django.urls import path 
from . import views 

app_name = "transactions_module"
urlpatterns = [
    path('checkout',views.checkout, name="checkout"),
    # Accept Membership

]