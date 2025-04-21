import requests
import json
from django.conf import settings
import uuid
#customers
from urllib.parse import urlencode
from django.http import JsonResponse
 
def generate_idempotency_key():
    return str(uuid.uuid4()).replace("-", "")[:25]

idempotency_key = generate_idempotency_key()


def idempotency_key_uuid(size=36):
  """
  Generates a UUID string of the specified size.

  Args:
    size: The desired length of the UUID string. Defaults to 36 (standard UUID length).

  Returns:
    A UUID string of the specified size.
  """
  if size == 36:
    return str(uuid.uuid4())
  elif size < 36:
    return str(uuid.uuid4()).replace("-", "")[:size]
  else:
    return str(uuid.uuid4()).replace("-", "")[:size]



def generate_alphanumeric_uuid_25():
    full_uuid = str(uuid.uuid4()).replace("-", "")  # Remove hyphens
    return full_uuid[:25]  # Ensure exactly 25 alphanumeric characters

def generate_full_uuid():
    return str(uuid.uuid4())  # Standard 36-character UUID

# Generate and print both UUIDs
uuid_25 = generate_alphanumeric_uuid_25()
full_uuid = generate_full_uuid()


def test_helcim_connection():
    url = "https://api.helcim.com/v2/connection-test"
    headers = {
        "accept": "application/json",
        "api-token": settings.HELCIM_API_TOKEN
    }
    try:
        response = requests.get(url, headers=headers)
        print("API Response Text:", response.text)  # Debugging

        response.raise_for_status()  # Raises an exception for HTTP errors (4xx, 5xx)

        try:
            response_dict = response.json()  # Parse response as JSON
        except json.JSONDecodeError:
            print("Error decoding JSON:", response.text)
            return {"error": "Invalid JSON response", "status_code": response.status_code, "raw_response": response.text}

        return {"data": response_dict, "status_code": response.status_code}  # Return both response and status code
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return {"error": str(e), "status_code": 500}  # Return error message with status code

    
    
def get_customer(api_token=None,usr_id=None):
    
    url = f"https://api.helcim.com/v2/customers/CST{usr_id}"
    
    headers = {
        "accept": "application/json",
        "api-token": settings.HELCIM_API_TOKEN
    }
    
    response = requests.get(url, headers=headers)
    
    print(response.text)
    return response.text


# Ensure settings is imported

def create_customer_helcim(usr_data=None):
    url = "https://api.helcim.com/v2/customers/"

    if not usr_data or not usr_data.get("email") or usr_data["email"].strip() == "":
        return {"error": "email not provided", "status_code": 400}

    # Keep payload as it is
    payload = {
        "billingAddress": {
            "name": usr_data.get("full_name", ""),  # Assigning contact or business name
            "street1": usr_data.get("street1", ""),  # Combining multiple fields for street address
            "street2": usr_data.get("street2", ""),
            "city": usr_data.get("city", ""),
            "province": usr_data.get("province", ""),  # State abbreviation (e.g., GA, NY)
            "country": usr_data.get("country", "USA"),  # Default to USA
            "postalCode": usr_data.get("postalCode", ""),
            "phone": usr_data.get("phone", ""),
            "email": usr_data.get("email", ""),
        },
        "customerCode": usr_data.get("customerCode", ""),
        "contactName": usr_data.get("full_name", ""),  # Use full_name for contact
        #"businessName": usr_data.get("full_name", ""),  # If it's a business, assign full_name
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-token": settings.HELCIM_API_TOKEN  # Ensure this is correctly set
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print("API Response Text:", response.text)  # Debugging

        response.raise_for_status()  # Raises an exception for HTTP errors (4xx, 5xx)

        try:
            response_dict = response.json()  # Parse response as JSON
        except json.JSONDecodeError:
            print("Error decoding JSON:", response.text)
            return {"error": "Invalid JSON response", "status_code": response.status_code, "raw_response": response.text}

        return {"data": response_dict, "status_code": response.status_code}  # Return both response and status code

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return {"error": str(e), "status_code": 500}  # Return error message with status code



#Generate  Checkout Token for Helcim.jsPay Frontedn Part where we adding card againts customer which customer code we pass here.
def checkout_session(api_token=None, usr_id=None,*args, **kwargs):
    """ 
       Creates a HelcimPay.js Checkout Session

    """
    url = "https://api.helcim.com/v2/helcim-pay/initialize"
    
    payload = {
        # "customerRequest": {
        #     # "billingAddress": {
        #     #     "name": "John Smith/Helcim",
        #     #     "street1": "22 Main Road",
        #     #     "street2": "s",
        #     #     "city": "Calgary",
        #     #     "province": "AB",
        #     #     "postalCode": "H0H0H0"
        #     # },
        #     "customerCode": f"CST{usr_id}",
        #     "contactName": f"{contact_name}"
        # },
        "paymentType": "verify",
        "amount": 0,
        "currency": "USD",
        "customerCode": f"CST{usr_id}",
        "paymentMethod": "cc",
        # "taxAmount": 3.67,
        # "hasConvenienceFee": 1,
        # "allowPartial": 1,
        # "invoiceNumber": "INV1000",
        # "hideExistingPaymentDetails": 1,
        # "setAsDefaultPaymentMethod": 1,
        # "terminalId": 1,
        "confirmationScreen": True
    }
    headers = {
        "accept": "application/json",
        "api-token": settings.HELCIM_API_TOKEN,
        "content-type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    #(response.text)
    response_dict = json.loads(response.text)
    checkout_token = response_dict["checkoutToken"]
    #print(checkout_token)
    return checkout_token


#Recurring API Setup
def get_plan(paymentPlanId=None):
    if not paymentPlanId:
        return None
    url = f"https://api.helcim.com/v2/payment-plans/{paymentPlanId}"
    
    headers = {
        "accept": "application/json",
        "api-token": settings.HELCIM_API_TOKEN,
    }
    
    response = requests.get(url, headers=headers)
    
    print(response.text)
    return response.text

from decimal import Decimal

def create_plans(name=None, setup_amount=0.0, recurring_amount=0.0):
    url = "https://api.helcim.com/v2/payment-plans"

    setup_amount = float(setup_amount) if isinstance(setup_amount, Decimal) else setup_amount
    recurring_amount = float(recurring_amount) if isinstance(recurring_amount, Decimal) else recurring_amount
    payload = {
        "paymentPlans": [
            {
                "type": "subscription",
                "billingPeriod": "monthly",
                "termType": "forever",
                "paymentMethod": "card",
                "name": name or "Default Plan Name",  # fallback if name is None
                "status": "active",
                "setupAmount": setup_amount,
                "recurringAmount": recurring_amount,
                "billSetupImmediately": "first_billing",
                "billingPeriodIncrements": 1,
                "dateBilling": "Sign-up"
            }
        ]
    }

    headers = {
        "accept": "application/json",
        "api-token": settings.HELCIM_API_TOKEN,  # Replace with real token
        "content-type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print("API Response Text:", response.text)  # Debugging

        response.raise_for_status()  # Raises an exception for HTTP errors (4xx, 5xx)

        try:
            response_dict = response.json()  # Parse response as JSON
            print(response_dict)
        except json.JSONDecodeError:
            print("Error decoding JSON:", response.text)
            return {"error": "Invalid JSON response", "status_code": response.status_code, "raw_response": response.text}

        return {"data": response_dict, "status_code": response.status_code}  # Return both response and status code
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return {"error": str(e), "status_code": 500}  # Return error message with status code

def delete_plan(paymentPlanId=None):
    ''' 
      dataType : 
      paymentPlanId : int
    '''
    url = f"https://api.helcim.com/v2/payment-plans/{paymentPlanId}"
    headers = {
        "accept": "application/json",
        "api-token": settings.HELCIM_API_TOKEN,
    }
    
    try:
        response = requests.delete(url, headers=headers)
        print(response.text)
        response.raise_for_status()  # Raises an exception for HTTP errors (4xx, 5xx
        try:
            response_dict = response.json()  # Parse response as JSON
        except json.JSONDecodeError:
            print("Error decoding JSON:", response.text)
            return {"error": "Invalid JSON response", "status_code": response.status_code, "raw_response": response.text}
        return {"status_code": response.status_code}  # Return both response and status code
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return {"error": str(e), "status_code": 500}  # Return error message with status code




def create_subscription(paymentPlanId=None,usr_id=None,dateActive=None):
    if not paymentPlanId:
        return None

    url = "https://api.helcim.com/v2/subscriptions"
    
    payload = { "subscriptions": [{
                "paymentMethod": "card",
                "paymentPlanId": paymentPlanId,
                "customerCode": f"CST{usr_id}",
                "useCustomSetupAmount": True,
                "setupAmount": 0.2,
                "recurringAmount": 0,
                "withFreeTrialPeriod": False,
                "dateActivated": dateActive,
            }, { "paymentMethod": "card" }] }
    headers = {
        "accept": "application/json",
        "api-token": settings.HELCIM_API_TOKEN,
        "idempotency-key": uuid_25,
        "content-type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print("API Response Text:", response.text)  # Debugging

        response.raise_for_status()  # Raises an exception for HTTP errors (4xx, 5xx)

        try:
            response_dict = response.json()  # Parse response as JSON
        except json.JSONDecodeError:
            print("Error decoding JSON:", response.text)
            return {"error": "Invalid JSON response", "status_code": response.status_code, "raw_response": response.text}

        return {"data": response_dict, "status_code": response.status_code}  # Return both response and status code

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return {"error": str(e), "status_code": 500}  # Return error message with status code


def delete_subscription():
    pass

def update_subscription(subscription_id=None, status="active"):
    url = "https://api.helcim.com/v2/subscriptions"
    payload = { "subscriptions": [
            {
                "id": subscription_id,
                "status": status or "paused",
            }
        ] }
    headers = {
        "accept": "application/json",
        "api-token": settings.HELCIM_API_TOKEN,
        "content-type": "application/json"
    }
    
    try:
        response = requests.patch(url, json=payload, headers=headers)
        print("API Response Text:", response.text)  # Debugging

        response.raise_for_status()  # Raises an exception for HTTP errors (4xx, 5xx)

        try:
            response_dict = response.json()  # Parse response as JSON
        except json.JSONDecodeError:
            print("Error decoding JSON:", response.text)
            return {"error": "Invalid JSON response", "status_code": response.status_code, "raw_response": response.text}

        return {"data": response_dict, "status_code": response.status_code}  # Return both response and status code

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return {"error": str(e), "status_code": 500}  # Return error message with status code

    