from django.urls import path
from apiroot.transactions.views import subscription_api,checkout_view,subscription_manage_api

urlpatterns = [
    path('subscription-api/', subscription_api, name='subscription_api'),
    path('subscription-manage-api/', subscription_manage_api, name='subscription_manage_api'),
    path('checkout-card/', checkout_view, name='checkout_card_api'),
    # if we gone use as_view() : AttributeError: 'function' object has no attribute 'as_view'

]