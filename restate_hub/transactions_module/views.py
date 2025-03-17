from django.shortcuts import render

# Create your views here.
from transactions_module.helcim import payment_process

def checkout(request):
    payment_process()
    return render(request, "transaction/checkout.html")