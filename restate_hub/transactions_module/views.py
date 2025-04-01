from django.shortcuts import render,redirect
from django.http import JsonResponse
# Create your views here.
from transactions_module.helcim import  CustomerDataService ,checkout_session , create_subscription

from transactions_module.paymone import capture_payment_info ,generate_idempotency_key

def checkout(request):
    #customer_data = customer_service.get_customer_data()
    #customer_service = CustomerDataService(request.user)
    #print(customer_data)
    checkoutcode = None
    # checkoutcode = checkout_session(usr_id=request.user.id)
    # print(checkoutcode)
    return render(request, "transaction/checkout.html", {'checkoutcode':checkoutcode})



