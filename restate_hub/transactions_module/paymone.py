import requests
import json
from django.conf import settings
import uuid
#customers
import requests
from django.conf import settings


import uuid
import random
import string

import uuid
import base64

def generate_idempotency_key():
    # Generate UUID (16 bytes binary form)
    uuid_bytes = uuid.uuid4().bytes

    # Encode in Base64, remove padding `=`, and take the first 25 characters
    idempotency_key = base64.urlsafe_b64encode(uuid_bytes).decode('utf-8').rstrip('=')[:25]

    return idempotency_key








#Recurring Payment Steps
api_token = settings.HELCIM_API_TOKEN

def capture_payment_info(*args, **kwargs):
    url = "https://api.helcim.com/v2/helcim-pay/initialize"
    payload = {
        "paymentType": "verify",
        "amount": 0,
        "currency": "USD",
        "customerCode": "CST19",
        "paymentMethod": "cc",
        "confirmationScreen": True
    }
    headers = {
        "accept": "application/json",
        "api-token":api_token,
        "content-type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    verified = response.text
    print(verified)
    response_dict = json.loads(response.text)
    checkout_token = response_dict["checkoutToken"]
    print(checkout_token)

  

  