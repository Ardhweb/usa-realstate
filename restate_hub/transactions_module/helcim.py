import requests
import json
from django.conf import settings
import uuid
#customers
import requests
from django.conf import settings

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

print("Custom 25-char Alphanumeric UUID:", uuid_25)
print("Full UUID:", full_uuid)

from urllib.parse import urlencode

class CustomerDataService:
    def __init__(self, user):
        self.user = user
        self.member_type = f"{self.user.member_type}s"  # Example: 'buyer' → 'buyers'
        
        # Dynamically get the related object (if it exists)
        self.related_member = getattr(self.user, self.member_type, None)
        
        # If it's a related manager (reverse relationship), get the first object
        self.instance_member = self.related_member if self.related_member else None
        # self.buyer =  self.user.buyers 
        self.address = self.instance_member.memberaddress_set.first() if self.instance_member else None  # Get first address

    def get_customer_data(self):
        if self.user.member_type not in ['buyer', 'seller', 'agent']:
            return None  # Or return {}
        return {
            "customerCode": f"CST{self.user.id}",
            "full_name": f"{self.instance_member.first_name}{self.instance_member.last_name}" if self.instance_member else "",
            "email": self.user.email,
            "phone": getattr(self.instance_member, "phone_num", ""),

            # # Member Address Fields
            "street1": f"{self.address.street_no} {self.address.street_name}" if self.address else "",
            "street2": self.address.suite_no if self.address else "",
            "country": "USA",
            "city": self.address.city if self.address else "",
            "province": self.address.state[:2].upper() if self.address and self.address.state else "",
            "postal_code": self.address.zip_code if self.address else "",
        }



from django.http import JsonResponse


def get_customer(api_token=None,usr_id=None):
    
    url = f"https://api.helcim.com/v2/customers/CST{usr_id}"
    
    headers = {
        "accept": "application/json",
        "api-token": settings.HELCIM_API_TOKEN
    }
    
    response = requests.get(url, headers=headers)
    
    print(response.text)
    return response.text


import requests
import json
from django.http import JsonResponse
from django.conf import settings  # Ensure settings is imported

def create_customer_helcim(usr_data=None):
    url = "https://api.helcim.com/v2/customers/"

    if not usr_data or not usr_data.get("email") or usr_data["email"].strip() == "":
        return {"error": "email not provided", "status_code": 400}

    # Keep payload as it is
    payload = {
        # "billingAddress": {
        #     "name": usr_data.get("full_name", ""),  # Assigning contact or business name
        #     "street1": usr_data.get("street1", ""),  # Combining multiple fields for street address
        #     "street2": usr_data.get("street2", ""),
        #     "city": usr_data.get("city", ""),
        #     "province": usr_data.get("province", ""),  # State abbreviation (e.g., GA, NY)
        #     "country": usr_data.get("country", "USA"),  # Default to USA
        #     "postalCode": usr_data.get("postal_code", ""),
        #     "phone": usr_data.get("phone", ""),
        #     "email": usr_data.get("email", ""),
        # },
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
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(response.text)
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


def test_connection():
  
    url = "https://api.helcim.com/v2/connection-test"
    
    headers = {
        "accept": "application/json",
        "api-token": settings.HELCIM_API_TOKEN
    }
    
    response = requests.get(url, headers=headers)
    
    print(response.text)