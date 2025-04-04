from django.urls import path 
from . import views 

app_name = "transactions_module"
urlpatterns = [
    path('checkout',views.checkout, name="checkout"),
    path('subscribe',views.subscribe_process, name="subscribe"),
    path("process-setup-billing", views.process_setup, name="process_setup"),
    path('process-checkout-add-card',views.process_checkout_add_card, name="process_checkout_add_card"),
    path('confirm-subscription', views.confirm_subscription, name="confirm_subscription"),
    # Accept Membership


]