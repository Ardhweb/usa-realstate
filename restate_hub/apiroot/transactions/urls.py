from django.urls import path
from apiroot.transactions.views import subscription_api,checkout_view

urlpatterns = [
    path('subscription-api/', subscription_api, name='subscription_api'),
    path('checkout-card/', checkout_view, name='checkout_card_api'),
    # if we gone use as_view() : AttributeError: 'function' object has no attribute 'as_view'

]