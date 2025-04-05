from django.urls import path 
from . import views 

app_name = "transactions_module"
urlpatterns = [
    path("process-setup-billing", views.process_setup, name="process_setup"),
    path('process-checkout-add-card',views.process_checkout_add_card, name="process_checkout_add_card"),
    # Accept Membership
    path('test', views.test_page, name="test_page"),


]